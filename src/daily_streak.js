// Daily question streaks, shared by the public /daily/ pages and every trainer. Inlined into
// both at build time, so there is exactly one definition of what a streak is.
//
// What a streak counts, and why. The trainer's first version reset the streak to zero on a
// wrong answer, which made it an accuracy streak wearing a habit's name. The research is
// consistent that the habit is the thing worth protecting. Silverman and Barasch in the
// Journal of Consumer Research found an intact streak raises later engagement and a broken
// one lowers it (academic.oup.com/jcr/article-abstract/49/6/1095/6623414); Chess.com keeps
// a daily puzzle streak alive at zero hearts (support.chess.com, "How does the Daily Puzzle
// work?"); Duolingo reports more daily learners after letting people hold a second streak
// freeze (blog.duolingo.com/how-duolingo-streak-builds-habit). All read 2026-09-26. So:
//
//   streak     consecutive days a question was answered, right or wrong. Today not yet
//              answered does not break it.
//   freezes    one earned for every seven consecutive days answered, at most two banked,
//              spent automatically on a missed day. Earned, never sold.
//   run        consecutive answered days that were all correct, kept as a personal best.
//              This is the accuracy record, and it is only ever compared with your own.
//
// Stored only in this browser (localStorage), under one key for every exam, so a day
// answered on the public page counts in the trainer and the reverse. Nothing here is sent
// anywhere, and there is no leaderboard to send it to.
var SFNDaily = (function () {
  var KEY = 'sfn_daily_v1';
  function load() {
    try { var v = JSON.parse(localStorage.getItem(KEY)); if (v && v.exams) return v; } catch (e) {}
    return { v: 1, exams: {} };
  }
  function save(v) { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {} }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  // The visitor's own calendar date, which is what "today's question" means to them.
  function today(d) { d = d || new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  function next(iso) {
    var p = iso.split('-'), d = new Date(+p[0], +p[1] - 1, +p[2] + 1);
    return today(d);
  }
  function days(slug) { var e = load().exams[slug]; return (e && e.days) || {}; }
  // The first answer for a date is the one that counts; a second attempt changes nothing.
  function record(slug, date, correct, secs, chosen) {
    var v = load();
    var e = v.exams[slug] || (v.exams[slug] = { days: {} });
    if (e.days[date]) return false;
    e.days[date] = { c: correct ? 1 : 0, s: Math.max(0, Math.round(secs || 0)) };
    if (typeof chosen === 'number') e.days[date].ch = chosen;
    save(v);
    return true;
  }
  function stats(slug, onDate) {
    var ds = days(slug), t = onDate || today();
    var keys = Object.keys(ds).filter(function (k) { return k <= t; }).sort();
    var out = { current: 0, best: 0, freezes: 0, run: 0, bestRun: 0, answered: keys.length,
                correct: keys.filter(function (k) { return ds[k].c; }).length,
                doneToday: !!ds[t], todayCorrect: ds[t] ? !!ds[t].c : null,
                todaySecs: ds[t] ? ds[t].s : null };
    if (!keys.length) return out;
    var since = 0, guard = 0;
    for (var d = keys[0]; d <= t && guard < 4000; d = next(d), guard++) {
      var e = ds[d];
      if (e) {
        out.current++; since++;
        if (since === 7) { out.freezes = Math.min(2, out.freezes + 1); since = 0; }
        if (e.c) { out.run++; out.bestRun = Math.max(out.bestRun, out.run); } else out.run = 0;
      } else if (d === t) {
        // Today, not answered yet: nothing is lost until the day is over.
      } else if (out.freezes > 0) {
        out.freezes--;
      } else {
        out.current = 0; since = 0; out.run = 0;
      }
      out.best = Math.max(out.best, out.current);
    }
    return out;
  }
  function clock(secs) {
    secs = Math.max(0, Math.round(secs || 0));
    return Math.floor(secs / 60) + ':' + pad(secs % 60);
  }
  // Spoiler free by construction: the exam, the date, right or wrong, the time and the
  // streak. Never the question and never the answer, so a post cannot give it away.
  function shareText(slug, examShort, date, correct, secs, streak) {
    var p = date.split('-');
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var when = months[+p[1] - 1] + ' ' + (+p[2]);
    return 'Start From Nowhere, ' + examShort + ' daily question, ' + when + '\n' +
      (correct ? '🟩 Solved in ' + clock(secs) : '🟥 Missed it, answered in ' + clock(secs)) +
      (streak > 1 ? ', ' + streak + ' day streak' : '') + '\n' +
      'https://startfromnowhere.com/daily/' + slug + '/';
  }
  return { KEY: KEY, load: load, today: today, next: next, days: days, record: record,
           stats: stats, clock: clock, shareText: shareText };
})();
