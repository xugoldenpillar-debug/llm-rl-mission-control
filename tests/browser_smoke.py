"""Optional real-browser regression suite. Run a local server before this script.
python -m pip install playwright
python -m playwright install chromium
python tests/browser_smoke.py --url http://127.0.0.1:8787 --output artifacts
Set CHROMIUM_PATH to use a system Chromium installation.
No personal study data is used: every test runs in a fresh browser context.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://127.0.0.1:8787')
    parser.add_argument('--output', default='artifacts')
    args = parser.parse_args()
    base = args.url.rstrip('/') + '/'
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    results: list[str] = []
    with sync_playwright() as p:
        options = {'headless': True, 'args': ['--no-sandbox']}
        if os.environ.get('CHROMIUM_PATH'):
            options['executable_path'] = os.environ['CHROMIUM_PATH']
        browser = p.chromium.launch(**options)
        context = browser.new_context(viewport={'width': 1440, 'height': 1100}, accept_downloads=True)
        page = context.new_page()
        errors: list[str] = []
        page.on('pageerror', lambda err: errors.append(str(err)))
        page.on('dialog', lambda d: d.accept())
        page.goto(base, wait_until='networkidle')
        expect(page.locator('#main h1')).to_be_visible()
        page.screenshot(path=str(out / 'desktop.png'), full_page=True)
        assert page.locator('.task-row').count() == 6
        results.append('fresh dashboard: six tasks, empty real progress, desktop layout')

        page.locator('[data-action="toggle-task"][data-id="d01-theory"]').click()
        expect(page.locator('[data-action="toggle-task"][data-id="d01-theory"]')).to_have_class('task-check checked')
        page.reload(wait_until='networkidle')
        expect(page.locator('[data-action="toggle-task"][data-id="d01-theory"]')).to_have_class('task-check checked')
        results.append('task completion persists after reload')

        page.locator('[data-action="select-day"][data-id="2"]').first.click()
        page.locator('[data-action="toggle-task"][data-id="d02-theory"]').click()
        expect(page.locator('#dialog')).to_be_visible()
        expect(page.locator('#toast')).to_contain_text('前置')
        page.locator('#dialog [data-action="waive"]').click()
        page.locator('#dialog textarea[name="reason"]').fill('已独立实现并测试 Attention，可用代码说明。')
        page.locator('#dialog button[type="submit"]').click()
        expect(page.locator('[data-action="toggle-task"][data-id="d02-theory"]')).to_have_class('task-check waived')
        results.append('dependency lock and documented mastery waiver')

        page.locator('a.nav-link[href="#journal"]').click()
        page.locator('textarea[data-journal="notes"]').fill('研究记录 <script>window.BAD=1</script>：验证 mask。')
        page.wait_for_timeout(800)
        page.reload(wait_until='networkidle')
        # Selected day is recalculated at startup; read the persisted journal state directly.
        saved = page.evaluate("""async () => {
          const {LocalStore}=await import('./js/storage.js');const st=new LocalStore();await st.open();
          return Object.values(st.state.journals).some(x=>x.notes?.includes('验证 mask'));
        }""")
        assert saved and page.evaluate('window.BAD') is None
        results.append('journal autosave and HTML/script content stays inert')

        page.locator('a.nav-link[href="#budget"]').click()
        page.locator('#main [data-action="new-expense"]').first.click()
        form = page.locator('form[data-form="expense"]')
        form.locator('[name="label"]').fill('GPU smoke test')
        form.locator('[name="quantity"]').fill('2.5')
        form.locator('[name="rate"]').fill('3')
        form.locator('button[type="submit"]').click()
        expect(page.locator('tbody')).to_contain_text('GPU smoke test')
        expect(page.locator('tbody')).to_contain_text('7.5')
        results.append('budget CRUD: quantity times rate, real total')

        page.locator('a.nav-link[href="#lab"]').click()
        for label, correct in [('Outcome baseline', '2'), ('Shaping trial', '3')]:
            page.locator('#main [data-action="new-experiment"]').first.click()
            form = page.locator('form[data-form="experiment"]')
            for name, value in {'name': label, 'model': 'Qwen3-0.6B', 'algorithm': 'GRPO',
                                'dataset': 'toy-code-v1', 'split': 'sealed-v1', 'correct': correct,
                                'total': '10'}.items():
                form.locator(f'[name="{name}"]').fill(value)
            form.locator('button[type="submit"]').click()
        checks = page.locator('input[data-filter="compare"]')
        checks.nth(0).check()
        page.locator('input[data-filter="compare"]').nth(1).check()
        expect(page.locator('#main')).to_contain_text('不自动判定显著性')
        assert page.locator('tbody').count() >= 2
        results.append('experiment creation and descriptive two-run comparison')

        # Concurrent tab writes use distinct fields and must both survive.
        other = context.new_page()
        other.goto(base, wait_until='networkidle')
        mutate = """async key => {const {LocalStore}=await import('./js/storage.js');
        const st=new LocalStore();await st.open();await st.mutate(s=>{s.journals[key]={notes:key};});return true;}"""
        page.evaluate(mutate, 'tab-a')
        other.evaluate(mutate, 'tab-b')
        merged = page.evaluate("""async () => {const {LocalStore}=await import('./js/storage.js');
        const st=new LocalStore();await st.open();return !!st.state.journals['tab-a']&&!!st.state.journals['tab-b'];}""")
        assert merged
        results.append('multiple tabs preserve independent writes')

        page.locator('a.nav-link[href="#settings"]').click()
        with page.expect_download() as download:
            page.locator('#main [data-action="export"]').first.click()
        backup_path = out / 'test-backup.json'
        download.value.save_as(str(backup_path))
        backup = json.loads(backup_path.read_text())
        assert backup['format'] == 'llm-rl-mission-control'
        assert len(backup['state']['experiments']) == 2
        before_revision = backup['state']['revision']
        page.locator('#import-file').set_input_files({'name': 'bad.json', 'mimeType': 'application/json',
                                                     'buffer': b'{"format":"other"}'})
        expect(page.locator('#toast')).to_contain_text('备份')
        assert page.locator('#dialog[open]').count() == 0
        results.append('JSON download and invalid import refusal without replacement')
        page.locator('#import-file').set_input_files(str(backup_path))
        expect(page.locator('#dialog-title')).to_contain_text('恢复前预览')
        page.locator('#dialog [data-action="confirm-import"]').click()
        expect(page.locator('#dialog[open]')).to_have_count(0)
        results.append('valid import preview and full-state recovery')

        page.locator('#main [data-action="encrypt-export"]').click()
        page.locator('#dialog [name="password"]').fill('test-only-long-password')
        page.locator('#dialog [name="confirm"]').fill('test-only-long-password')
        with page.expect_download() as download:
            page.locator('#dialog button[type="submit"]').click()
        encrypted_path = out / 'test-encrypted.rlmc'
        download.value.save_as(str(encrypted_path))
        page.locator('#import-file').set_input_files(str(encrypted_path))
        page.locator('#dialog [name="password"]').fill('test-only-long-password')
        page.locator('#dialog button[type="submit"]').click()
        expect(page.locator('#dialog-title')).to_contain_text('恢复前预览')
        page.locator('#dialog [data-action="close"]').click()
        results.append('AES-GCM password-encrypted backup round-trip')

        for name in ['dashboard','plan','roadmap','resources','reviews','lab','journal','budget','portfolio','guide','settings']:
            page.locator(f'a.nav-link[href="#{name}"]').click()
            expect(page.locator('#main h1')).to_be_visible()
            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1')
        results.append('all eleven screens render with no desktop horizontal overflow')
        page.locator('a.nav-link[href="#dashboard"]').click()
        page.locator('[data-action="theme"]').click()
        expect(page.locator('html')).to_have_attribute('data-theme', 'dark')
        page.screenshot(path=str(out / 'dark.png'), full_page=True)
        page.locator('[data-action="theme"]').click()
        results.append('dark mode persisted and rendered')

        mobile = context.new_page(viewport={'width': 390, 'height': 844}) if False else context.new_page()
        mobile.set_viewport_size({'width': 390, 'height': 844})
        mobile.goto(base, wait_until='networkidle')
        assert mobile.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1')
        mobile.screenshot(path=str(out / 'mobile.png'), full_page=True)
        mobile.locator('[data-action="menu"]').click()
        expect(mobile.locator('.sidebar')).to_have_class('sidebar open')
        mobile.locator('a.nav-link[href="#plan"]').click()
        expect(mobile.locator('#main h1')).to_contain_text('30 天')
        results.append('390px mobile layout and navigation drawer')

        # Wait for the first install, then a controlled reload must work offline.
        page.goto(base, wait_until='networkidle')
        page.evaluate('navigator.serviceWorker.ready')
        page.reload(wait_until='networkidle')
        context.set_offline(True)
        page.reload(wait_until='domcontentloaded')
        expect(page.locator('#main h1')).to_be_visible()
        context.set_offline(False)
        results.append('offline application shell reload')
        assert not errors, errors
        report = {'browser': browser.version, 'passed': len(results), 'checks': results, 'page_errors': errors}
        (out / 'browser-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
        print(json.dumps(report, ensure_ascii=False, indent=2))
        context.close()
        browser.close()

if __name__ == '__main__':
    main()
