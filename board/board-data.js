// Demo board data (restructured into five stops Nov 10). Lesson and story slides are the locked deck's words (Workshop v16.3 + Offer v11).
// kind: teach | watch | turn | bonus | title | photo
var SITE = 'https://2guysandagenie.com';
var LESSONS = [
  { id: 'open', name: 'The open', sub: 'The promise, the wishes, the yes.', slides: [
    ['title', 'How To Take Your Business Places It\'s Never Been…', 'If you can talk, you can do this.'],
    ['teach', 'Today', 'The rules. Real businesses. Yours.'],
    ['title', 'The lamp', 'A genie shows up for your business. What do you wish for?'],
    ['teach', 'When you registered, you told us…', 'Read back two or three real answers.'],
    ['title', 'Who wants to do it all… just by talking?', ''],
    ['title', 'All you need is your phone.', '']
  ]},
  { id: 'story', name: 'Jimmy\'s story', sub: 'Rap Tips to tapping to the genie.', slides: [
    ['photo', 'Paul and Jimmy', '', SITE + '/assets/room-jimmy-paul.jpg'],
    ['photo', 'Twelve years old', 'Photo needed'],
    ['title', 'Rap Tips.', ''],
    ['photo', 'The rise', 'Photo needed'],
    ['title', 'Thirty-two.', ''],
    ['photo', 'Back home', 'Photo needed'],
    ['title', 'Rap Tips → Tapping', '$20,000,000+'],
    ['title', 'A year → a few days.', ''],
    ['title', 'The genie out of the lantern.', '']
  ]},
  { id: 'l1', name: 'Lesson one: curiosity', sub: 'Ask it out loud. Then the room asks theirs.', slides: [
    ['teach', 'Maximum Leverage', '"Give me a lever long enough and a place to stand, and I will move the world." Archimedes'],
    ['teach', 'Where it all begins', 'Curiosity.'],
    ['watch', 'Asked live', 'No typing. Just talking.'],
    ['turn', 'Ask AI something you\'re curious about.', 'No account? Make a free one now.'],
    ['teach', 'Who here can be curious?', 'Then you\'re in.']
  ]},
  { id: 'l2', name: 'Lesson two: the five rules', sub: 'No rules vs five rules, then the bonus moves.', slides: [
    ['teach', 'What\'s the catch?', 'It can\'t be that easy.'],
    ['teach', 'Lesson Two', 'Five Simple AI Rules'],
    ['teach', 'Rule 1', 'Tell it who it is.'],
    ['teach', 'Rule 2', 'Give it context.'],
    ['teach', 'Rule 3', 'Say exactly what you want back.'],
    ['teach', 'Rule 4', 'Don\'t take the first answer.'],
    ['teach', 'Rule 5', 'Use the right model.'],
    ['teach', 'Five Simple AI Rules', '1 Tell it who it is.|2 Give it context.|3 Say exactly what you want back.|4 Don\'t take the first answer.|5 Use the right model.'],
    ['watch', '"Help me find a Christmas gift for my wife."', 'One line. None of the rules.'],
    ['watch', 'Same gift.', 'All five rules.'],
    ['turn', 'Now you try.', 'A gift for someone you love.|1 Tell it who it is.|2 Give it context.|3 Say exactly what you want back.|4 Don\'t take the first answer.|5 Use the right model.'],
    ['turn', 'Different AIs give different answers.', 'Paste the same thing into a second free AI.'],
    ['bonus', 'Two more moves', 'for even better answers. Things I learned just by playing around.'],
    ['watch', 'Let it ask you.', '"Before you suggest anything, ask me five questions."'],
    ['bonus', 'On bigger jobs, check its thinking.', '"Show me your plan, and tell me what you\'re assuming."'],
    ['turn', 'Let it ask you.', 'Same gift. Before it suggests anything, have it ask you five questions.'],
    ['teach', 'How to get better', 'Find someone who does it well. Copy how they do it.'],
    ['title', 'Did any of that go over your head?', ''],
    ['title', 'You can do this, right?', 'Not complicated. You can go home and do this tonight.']
  ]}
];
// The night in five stops (Nov 10). Each stop lists its lesson squares and demo groups, in order.
var STAGES = [
  { id: 'who', n: 1, name: 'Who we are', note: 'Why AI is amazing, and why we\'re magic at it.', lessons: ['open', 'story'], groups: [] },
  { id: 'basics', n: 2, name: 'Two things tonight', note: 'Demo, let them go play, "come back to me," make it better. 10 to 15 minutes. They go home and these are different forever.', lessons: ['l1', 'l2'], groups: ['setup'] },
  { id: 'done', n: 3, name: 'What we\'ve done', note: 'Machine-gun the proof: show it, "get it?", move. Check in once after each big point, then keep going. Drop in a "you can too" between wins.', lessons: [], groups: ['sees', 'plate', 'money', 'shows', 'too'] },
  { id: 'yours', n: 4, name: 'Your turn', note: 'Pre-picked volunteers, 5 to 10 minutes each. Start the slow ones first and let them run in the background while you do the quick ones.', lessons: [], groups: ['yours'] },
  { id: 'close', n: 5, name: 'Two doors', note: '"We\'re out of time." Trial closes back to what they saw: would it be worth it? The Build at $4,997 or the Meeting at $997. Hand out the order forms. Spots fill fast. Go or not?', lessons: [], groups: ['close'] }
];
// ty: live (Jimmy runs it in AI; prompt is copied) | show (one click to the real thing)
// need: what's still missing (shows a marker) · note: what to say or watch for · bg: can run in the background · k: room label
var GROUPS = [
  ['setup', 'Set it up tonight'],
  ['sees', 'It sees what you can\'t'],
  ['plate', 'It takes work off your plate'],
  ['money', 'It brings in money, not just a website'],
  ['shows', 'Your business finally shows up'],
  ['too', 'You can too (quick asides)'],
  ['yours', 'On a business in the room'],
  ['close', 'The close']
];
var DEMOS = [
  { id: 'todo', g: 'setup', ty: 'live', t: 'A running to-do list', p: 'Say it once. It keeps track.',
    prompt: 'You\'re my assistant. Keep a running to-do list for me in this chat. When I tell you something to do, add it. When I say it\'s done, move it to a Done list. Show me the list every time it changes. Start with these three: [three things].' },
  { id: 'email', g: 'setup', ty: 'live', t: 'Your email, checked for you', p: 'Every morning, only what needs you.', need: 'Gmail connected in Claude on Jimmy\'s setup',
    prompt: 'Check my email from the last 24 hours. Show me only the messages that need an answer from me, with a one-line suggested reply for each. Put everything else in one short list I can skim. Never show me anything nasty word for word. Just tell me calmly what it\'s about.' },
  { id: 'job', g: 'setup', ty: 'live', t: 'The job I never want again', p: 'One daily job. One headache gone.',
    prompt: 'I\'m glad you\'re here. I don\'t ever want to have to do this again. Every morning, bring me only what I need to address. Anything extremely negative never goes in front of my face. Answer it, and show me a calm version of what\'s going on: \'This person needs a refund.\' \'This person never got their download.\' Help me turn those answers into a system, so I\'m never part of it again. And keep an eye out: if something keeps coming up, tell me whether it\'s a problem we can fix with a system, or just someone having a bad day. I want to know about the trend, not the negativity.' },
  { id: 'prospect', g: 'sees', ty: 'live', t: 'Read a prospect before you call', p: 'Who they are, what they mean, how they see you.', need: 'One of Jimmy\'s real chamber or association reads as the backup',
    prompt: 'I\'m meeting [name], [title] at [business], today. Look them up. Tell me who they are, what they care about, how they\'ll probably read a message from me, what questions they\'ll have about me, and the best way to open the conversation.' },
  { id: 'ian', g: 'sees', ty: 'show', t: 'Ian\'s business inside his business', p: 'A niche nobody owns. Now he leads it.', url: 'https://ineedjimmy.com/ianb/', need: 'Ian\'s niche and his live site' },
  { id: 'mccray', g: 'plate', ty: 'show', t: 'Dr. McCray\'s morning numbers', p: 'Every number he needs, every morning.', url: 'https://daegansmith.me/dr-mccray/', need: 'McCray\'s dashboard, a version safe for the big screen' },
  { id: 'maestro', g: 'plate', ty: 'show', t: 'Call the pizza shop', p: 'The AI answers and takes the order.', url: SITE + '/stories/maestros/', need: 'The phone number for the call' },
  { id: 'followup', g: 'plate', ty: 'show', t: 'Jamon\'s follow-up', p: 'From nothing to thank-you, review and referral.', url: SITE + '/stories/gotta-call-jack/', need: 'The messages themselves' },
  { id: 'ads', g: 'money', ty: 'show', t: 'Jamon\'s TV and radio ads', p: '$15,000 a month to over $50,000.', need: 'The ad files or links' },
  { id: 'jamonvid', g: 'money', ty: 'show', t: 'Jamon, in his own words', p: 'The video.', url: SITE + '/assets/jamon-testimonial.mp4' },
  { id: 'bread', g: 'money', ty: 'show', t: 'Jim\'s Amazing Bread', p: 'From losing money on every box.', url: 'https://jimsamazingbread.com', need: 'Jim\'s bread video' },
  { id: 'jimmission', g: 'money', ty: 'show', t: 'Jim: from bread to changing lives', p: 'His why, then partners who serve the same people.', url: 'https://jimsamazingbread.com', need: 'Jim\'s customer letters, and his daughter\'s story confirmed with Jim',
    note: 'The turn: his business isn\'t bread, it\'s changing lives. That opens partners who sell to the same healthy-living customers (water filters, supplements, yoga): my customers become yours, yours become mine.' },
  { id: 'estimate', g: 'money', ty: 'live', t: 'Jamon\'s estimate', p: 'One price becomes three.',
    prompt: 'Here\'s an estimate I gave for a job: a fence. Labor, materials, removal, permits. Total $7,000. Turn this into three options for the same job, good, better and best, with what\'s in each one and a price for each.' },
  { id: 'jackname', g: 'shows', ty: 'show', t: 'How we found GottaCallJack', p: 'Not magic. We noticed the thing.', url: 'https://gottacalljack.com', need: 'The steps Jimmy actually took to land the name',
    note: 'Ask, get an answer, choose what matters, refine, move it forward. Whatever you\'re good at, you get better at.' },
  { id: 'bruce', g: 'shows', ty: 'show', t: 'Bruce: a site with a personality', p: 'It feels like him.', url: 'https://ineedjimmy.com/bruce/', need: 'How Jimmy got Bruce\'s personality in' },
  { id: 'jack', g: 'shows', ty: 'show', t: 'TJOAT.net to GottaCallJack.com', p: 'Only how it shows up changed.', url: 'https://gottacalljack.com' },
  { id: 'wall', g: 'shows', ty: 'show', t: 'Neither were these', p: 'Lawyer, vape shop, photographer, DJ.', url: 'https://daegansmith.me/before-after.html' },
  { id: 'adobe', g: 'too', ty: 'show', t: 'One guy vs. Adobe', p: 'Seven Adobe apps rebuilt with AI in about a week. Free.', url: 'https://getartcraft.com/apps', need: 'Open the link once before the night to check it loads',
    note: 'Brandon Thomas, fed up with Adobe\'s subscription, used Claude to rebuild Photoshop, Illustrator, Premiere, Lightroom, After Effects, InDesign and Acrobat as free apps (ArtCraft). First code Sept 30, 2026; about eight days to all seven. Say "about a week," not "a day." They\'re early and rough, so show the idea, not a demo of the app.' },
  { id: 'house', g: 'too', ty: 'show', t: 'Run your house from anywhere', p: 'Lights, TV, all by voice. You can too.', need: 'Jimmy\'s Home Assistant clip, or a live command',
    note: 'Quick aside, then "now, back with me." Keep moving.' },
  { id: 'research', g: 'yours', ty: 'live', t: 'What\'s great about your site', p: 'What\'s cool, and what\'s hiding.',
    prompt: 'Here\'s a local business website: [URL]. What would a customer want to find that isn\'t there? What does this business do well that the site never says? Give me the three changes that would bring in the most calls.' },
  { id: 'loves', g: 'yours', ty: 'live', t: 'What your customers love', p: 'What they say that you never do.',
    prompt: 'Read the reviews and the website for [business, town]. What do customers love about them that the business never says anywhere? Quote the customers.' },
  { id: 'newlook', g: 'yours', ty: 'live', bg: true, t: 'A new look', p: 'Their home page, redesigned while we talk.', need: 'Practice run: how long it takes',
    prompt: 'Here\'s [business]\'s website: [URL]. Redesign their home page so it\'s the best-looking one in [town] for what they do. Keep their real name, phone number, photos and reviews. Lead with what customers love about them. Build it as one page I can open in a browser.' },
  { id: 'numbers', g: 'yours', ty: 'live', t: 'Your numbers', p: 'Where the money comes and goes.',
    prompt: 'I run [business]. Ask me five quick questions about my numbers, one at a time: what I charge, what it costs me, how many customers I get a month, how many come back, and where they come from. Then show me where I\'m making and losing money, and the one number to watch every morning.' },
  { id: 'customers', g: 'yours', ty: 'live', bg: true, t: 'More customers', p: 'Ways to bring in more, fast.',
    prompt: 'I run [business] in [town]. Give me ten ways to get more customers in the next 30 days that cost little or nothing, ranked by how fast they\'d bring in money. For the top three, write exactly what I\'d say or post.' },
  { id: 'offer', g: 'close', ty: 'show', k: 'The offer', t: 'The offer', p: 'The Build or the Meeting.', need: 'Offer v12 slides onto the board' },
  { id: 'orderform', g: 'close', ty: 'show', k: 'The offer', t: 'The order form', p: 'Paper, handed out. Fill it out quick.', url: SITE + '/print/enrollment-form.pdf' },
  { id: 'orderpage', g: 'close', ty: 'show', k: 'The offer', t: 'The order page', p: 'For anyone who\'d rather tap.', url: SITE + '/order/' }
];
