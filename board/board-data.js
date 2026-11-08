// Demo board data. Lesson and story slides are the locked deck's words (Workshop v16.3 + Offer v11).
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
// ty: live (Jimmy runs it in AI; prompt is copied) | show (one click to the real thing)
// need: what's still missing (shows a marker)
var GROUPS = [
  ['setup', 'Set it up tonight'],
  ['sees', 'It sees what you can\'t'],
  ['plate', 'It takes work off your plate'],
  ['money', 'It brings in money, not just a website'],
  ['shows', 'Your business finally shows up']
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
  { id: 'research', g: 'sees', ty: 'live', t: 'Research a real website', p: 'A volunteer\'s site: what\'s missing.',
    prompt: 'Here\'s a local business website: [URL]. What would a customer want to find that isn\'t there? What does this business do well that the site never says? Give me the three changes that would bring in the most calls.' },
  { id: 'loves', g: 'sees', ty: 'live', t: 'What your customers love', p: 'What they say that you never do.',
    prompt: 'Read the reviews and the website for [business, town]. What do customers love about them that the business never says anywhere? Quote the customers.' },
  { id: 'mccray', g: 'plate', ty: 'show', t: 'Dr. McCray\'s morning numbers', p: 'Every number he needs, every morning.', url: 'https://daegansmith.me/dr-mccray/', need: 'McCray\'s dashboard, a version safe for the big screen' },
  { id: 'maestro', g: 'plate', ty: 'show', t: 'Call the pizza shop', p: 'The AI answers and takes the order.', url: SITE + '/stories/maestros/', need: 'The phone number for the call' },
  { id: 'followup', g: 'plate', ty: 'show', t: 'Jamon\'s follow-up', p: 'From nothing to thank-you, review and referral.', url: SITE + '/stories/gotta-call-jack/', need: 'The messages themselves' },
  { id: 'ads', g: 'money', ty: 'show', t: 'Jamon\'s TV and radio ads', p: '$15,000 a month to over $50,000.', need: 'The ad files or links' },
  { id: 'jamonvid', g: 'money', ty: 'show', t: 'Jamon, in his own words', p: 'The video.', url: SITE + '/assets/jamon-testimonial.mp4' },
  { id: 'bread', g: 'money', ty: 'show', t: 'Jim\'s Amazing Bread', p: 'From losing money on every box.', url: 'https://jimsamazingbread.com', need: 'Jim\'s bread video' },
  { id: 'estimate', g: 'money', ty: 'live', t: 'Jamon\'s estimate', p: 'One price becomes three.',
    prompt: 'Here\'s an estimate I gave for a job: a fence. Labor, materials, removal, permits. Total $7,000. Turn this into three options for the same job, good, better and best, with what\'s in each one and a price for each.' },
  { id: 'bruce', g: 'shows', ty: 'show', t: 'Bruce: a site with a personality', p: 'It feels like him.', url: 'https://ineedjimmy.com/bruce/', need: 'How Jimmy got Bruce\'s personality in' },
  { id: 'jack', g: 'shows', ty: 'show', t: 'TJOAT.net to GottaCallJack.com', p: 'Only how it shows up changed.', url: 'https://gottacalljack.com' },
  { id: 'wall', g: 'shows', ty: 'show', t: 'Neither were these', p: 'Lawyer, vape shop, photographer, DJ.', url: 'https://daegansmith.me/before-after.html' }
];
