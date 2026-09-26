"""Additional destructive tests, always in isolated browser storage."""
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
    checks = []
    with sync_playwright() as p:
        launch = {'headless': True, 'args': ['--no-sandbox']}
        if os.environ.get('CHROMIUM_PATH'):
            launch['executable_path'] = os.environ['CHROMIUM_PATH']
        browser = p.chromium.launch(**launch)
        ctx = browser.new_context(viewport={'width': 1280, 'height': 1000})
        page = ctx.new_page()
        page.on('dialog', lambda d: d.accept())
        page.goto(base, wait_until='networkidle')
        other = ctx.new_page()
        other.goto(base, wait_until='networkidle')
        start_writes = """prefix => {
          window.writeDone=false;window.writeError=null;
          (async()=>{const {LocalStore}=await import('./js/storage.js');const s=new LocalStore();await s.open();
            for(let i=0;i<30;i++)await s.mutate(x=>{x.journals[prefix+i]={notes:prefix+i};});
          })().then(()=>window.writeDone=true).catch(e=>{window.writeError=String(e);window.writeDone=true;});
          return true;
        }"""
        page.evaluate(start_writes, 'A-')
        other.evaluate(start_writes, 'B-')
        page.wait_for_function('window.writeDone')
        other.wait_for_function('window.writeDone')
        assert page.evaluate('window.writeError') is None
        assert other.evaluate('window.writeError') is None
        result = page.evaluate("""async()=>{const {LocalStore}=await import('./js/storage.js');
          const s=new LocalStore();await s.open();return {count:Object.keys(s.state.journals).length,
          snapshots:(await s.snapshotList()).length};}""")
        assert result['count'] == 60, result
        assert 0 < result['snapshots'] <= 7, result
        checks.append('60 overlapping IndexedDB transactions across two tabs: no lost records; snapshots bounded')

        page.evaluate("""async()=>{const {LocalStore}=await import('./js/storage.js');
          const {dateKey}=await import('./js/core.js');const s=new LocalStore();await s.open();await s.mutate(x=>{
          x.timer={id:'integrity',mode:'focus',taskId:'d01-theory',date:dateKey(),durationMs:60000,
          remainingMs:60000,startedAt:Date.now()-61000,status:'running'};});}""")
        page.wait_for_timeout(2300)
        result = page.evaluate("""async()=>{const {LocalStore}=await import('./js/storage.js');
          const s=new LocalStore();await s.open();return {timer:s.state.timer,sessions:Object.values(s.state.sessions)};}""")
        assert result['timer'] is None
        assert len(result['sessions']) == 1
        assert result['sessions'][0]['minutes'] == 1
        page.reload(wait_until='networkidle')
        checks.append('expired timer is settled once across two tabs and remains settled after refresh')
        other.close()

        backup = page.evaluate("""async()=>{const {LocalStore}=await import('./js/storage.js');
          const {backupEnvelope}=await import('./js/core.js');const s=new LocalStore();await s.open();
          return JSON.stringify(backupEnvelope(s.state));}""")
        page.evaluate("""async()=>{const {LocalStore}=await import('./js/storage.js');const s=new LocalStore();await s.open();
          await new Promise((ok,no)=>{const t=s.db.transaction('data','readwrite');
          t.objectStore('data').put({schemaVersion:999,revision:'broken',unexpected:true},'root');t.oncomplete=ok;t.onerror=no;});}""")
        page.reload(wait_until='networkidle')
        expect(page.locator('.boot h1')).to_contain_text('数据需要安全恢复')
        page.locator('#import-file').set_input_files({'name': 'recovery.json', 'mimeType': 'application/json', 'buffer': backup.encode()})
        expect(page.locator('#dialog-title')).to_contain_text('恢复前预览')
        page.locator('#dialog [data-action="confirm-import"]').click()
        expect(page.locator('#main h1')).to_be_visible()
        recovered = page.evaluate("""async()=>{const {LocalStore}=await import('./js/storage.js');
          const s=new LocalStore();await s.open();return s.state;}""")
        assert recovered['schemaVersion'] == 1
        assert 'unexpected' not in recovered
        assert len(recovered['journals']) == 60
        checks.append('corrupted root is not silently reset; valid backup restores it without retaining unknown keys')
        ctx.close()

        # Full mobile navigation has to fit, including longer course/task content.
        mobile_ctx = browser.new_context(viewport={'width': 390, 'height': 844})
        mobile = mobile_ctx.new_page()
        mobile.goto(base, wait_until='networkidle')
        for view in ['plan','roadmap','resources','reviews','lab','journal','budget','portfolio','guide','settings','dashboard']:
            mobile.locator('[data-action="menu"]').click()
            mobile.locator(f'a.nav-link[href="#{view}"]').click()
            expect(mobile.locator('#main h1')).to_be_visible()
            assert mobile.evaluate('document.documentElement.scrollWidth <= innerWidth+1'), view
        mobile.screenshot(path=str(out / 'mobile-clean.png'), full_page=True)
        mobile.set_viewport_size({'width': 320, 'height': 740})
        assert mobile.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
        checks.append('all eleven views fit 390px; fresh dashboard also fits 320px')
        mobile_ctx.close()

        # Do not pretend storage is durable when the browser blocks both mechanisms.
        fallback_ctx = browser.new_context()
        fallback_ctx.add_init_script("""Object.defineProperty(window,'indexedDB',{get(){throw new Error('blocked in test')}});
          Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked in test')}});""")
        fallback = fallback_ctx.new_page()
        fallback.goto(base, wait_until='networkidle')
        expect(fallback.locator('#main h1')).to_be_visible()
        expect(fallback.locator('#save-status')).to_contain_text('仅内存')
        checks.append('blocked browser storage is visibly labeled memory-only, not falsely saved')
        fallback_ctx.close()

        report = {'browser': browser.version, 'passed': len(checks), 'checks': checks}
        (out / 'integrity-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
        print(json.dumps(report, ensure_ascii=False, indent=2))
        browser.close()

if __name__ == '__main__':
    main()
