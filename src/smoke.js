const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1280,height:900}});
 const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{ if(m.type()==='error') errs.push(m.text()); });
 await p.goto('file:///home/claude/gmat/index.html'); await p.waitForTimeout(800);
 await p.screenshot({path:'shot_dash.png',fullPage:false});
 await p.click("text=Start today's round"); await p.waitForTimeout(300);
 await p.screenshot({path:'shot_q1.png'});
 const isTpa=await p.$('.tpa'); if(isTpa){ await p.click('input[name=tpa0]'); await p.click('input[name=tpa1]'); } else { await p.click('#opt0'); }
 await p.click('#submitBtn'); await p.waitForTimeout(200); await p.screenshot({path:'shot_fb.png'});
 const wrong=await p.$('.reason button'); if(wrong){ await p.click('.reason button'); }
 await p.click('text=Next question'); await p.waitForTimeout(200);
 for(let i=0;i<9;i++){ const t=await p.$('.tpa'); if(t){ await p.click('input[name=tpa0]'); await p.click('input[name=tpa1]'); } else { await p.click('#opt1'); } await p.click('#submitBtn'); await p.waitForTimeout(100); const rb=await p.$('.reason button'); if(rb) await p.click('.reason button'); const nx=await p.$('text=Next question'); if(nx) await nx.click(); else { await p.click('text=See results'); } await p.waitForTimeout(100); }
 await p.screenshot({path:'shot_results.png',fullPage:true});
 await p.click('nav >> text=Dashboard'); await p.waitForTimeout(300); await p.screenshot({path:'shot_dash2.png',fullPage:true});
 await p.click('nav >> text=Review'); await p.waitForTimeout(200); await p.screenshot({path:'shot_review.png'});
 await p.click('nav >> text=Drill'); await p.waitForTimeout(200); await p.click('nav >> text=Playbook'); await p.click('nav >> text=Settings'); await p.waitForTimeout(200);
 await p.reload(); await p.waitForTimeout(500); const kpi=await p.textContent('.tile .v'); console.log('after reload first tile:',kpi.trim());
 console.log('errors:',errs); await b.close();
})();
