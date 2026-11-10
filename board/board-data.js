// Demo board data (seven stops since Nov 10). Lesson and story slides are the locked deck's words (Workshop v16.3 + Offer v11).
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
// The night in seven stops (Nov 10, 12:52pm). items: squares in this exact order (lessons and demos mixed). Otherwise lessons, then groups.
var STAGES = [
  { id: 'who', n: 1, name: 'Who we are', note: 'The open and Jimmy\'s story.', lessons: ['open', 'story'], groups: [] },
  { id: 'state', n: 2, name: 'The state of AI right now', note: 'Open the real pages and let Jimmy get them excited: what AI has solved, and how fast it\'s moving. End on: "You guys ready to learn?"', lessons: [], groups: ['smart'] },
  { id: 'basics', n: 3, name: 'The basics: let\'s teach you how', note: 'Ask it something. Refine it with the five rules. Then email, then the to-do list. The room does each one on their phones. "Done? Now the next one."', lessons: [], groups: [], items: ['l1', 'sk1', 'l2', 'sk3', 'sk2'] },
  { id: 'between', n: 4, name: 'In between: from the basics to the cool stuff', note: 'Parked here until Daegan places them. Some are room exercises, some lead into "let us show you the cool stuff": the job you dread pairs with Maestro\'s; a read on anyone leads into the marketing.', lessons: [], groups: ['skills'] },
  { id: 'done', n: 5, name: 'What we\'ve done', note: 'Machine-gun the proof: show it, "get it?", move. Check in once after each big point, then keep going. Drop in a "you can too" between wins.', lessons: [], groups: ['sees', 'plate', 'money', 'shows', 'too'] },
  { id: 'yours', n: 6, name: 'Your turn', note: 'Pre-picked volunteers, 5 to 10 minutes each. Start the slow ones first and let them run in the background while you do the quick ones.', lessons: [], groups: ['yours'] },
  { id: 'close', n: 7, name: 'Two doors', note: '"We\'re out of time." Trial closes back to what they saw: would it be worth it? The Build at $4,997 or the Meeting at $997. Hand out the order forms. Spots fill fast. Go or not?', lessons: [], groups: ['close'] }
];
// ty: live (Jimmy runs it in AI; prompt is copied) | show (one click to the real thing)
// need: what's still missing (shows a marker) · note: what to say or watch for · bg: can run in the background · k: room label
var GROUPS = [
  ['smart', 'How smart is AI?'],
  ['basics', 'The basics'],
  ['skills', 'Skills still looking for a home'],
  ['sees', 'It sees what you can\'t'],
  ['plate', 'It takes work off your plate'],
  ['money', 'It brings in money, not just a website'],
  ['shows', 'Your business finally shows up'],
  ['too', 'You can too (quick asides)'],
  ['yours', 'On a business in the room'],
  ['close', 'The close']
];
var DEMOS = [
  { id: "sk1", g: "basics", ty: "live", k: "Skill 1", t: "Just ask it something", p: "The first step. Out loud, no typing.", sites: [['The skill page', SITE + '/ready/?all=1#d1'], ["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: "sk2", g: "basics", ty: "live", k: "Skill 2", t: "The to-do list for life", p: "Every to-do out of your head, for good.", prompt: "You're keeping my to-do list from now on. Two parts: Today, and Everything Else. When I tell you something to do, add it and group it with things like it. If I say something I've already said, don't list it twice. Count it, like 'said 3 times,' so I can see what I keep putting off. When I say something's done, move it to a Done list at the bottom. Every time I come back, show me Today first, ask what I want to move onto Today, and ask about anything I didn't finish: keep it on Today, or move it back? Start now.", sites: [['The skill page', SITE + '/ready/?all=1#d2'], ["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: "sk3", g: "basics", ty: "live", k: "Skill 3", t: "Have AI read your inbox", p: "Your morning email, sorted for you.", prompt: "Check my inbox. List the emails from this week that still need a reply from me, most important first.", need: "Which plan each app needs to connect email; a privacy answer ready for the room", sites: [['The skill page', SITE + '/ready/?all=1#d3'], ["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: "sk4", g: "skills", ty: "live", k: "Skill 4", t: "Hand AI the job you dread", p: "Three ways to get it off your plate.", prompt: "I run a [your kind of business] in [your town]. The job I dread most is [your job]. Ask me three questions about it, one at a time. Then show me three ways you could take it off my plate.", sites: [['The skill page', SITE + '/ready/?all=1#d4'], ["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: "sk5", g: "skills", ty: "live", k: "Skill 5", t: "Your business through a stranger's eyes", p: "One photo of your truck, sign or card.", prompt: "You're a stranger seeing this for the first time. What does this business do? And what would you never guess about it?", sites: [['The skill page', SITE + '/ready/?all=1#d5'], ["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: "sk6", g: "skills", ty: "live", k: "Skill 6", t: "Your missed-call number", p: "The customers who picked you and never got you.", sites: [['The skill page', SITE + '/ready/?all=1#d6'], ["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: "sk7", g: "skills", ty: "live", k: "Skill 7", t: "Your website in five seconds", p: "What a stranger misses.", prompt: "Here's my website: [your address]. You're a stranger who needs what I sell. You've got five seconds. What do you see? And what's the best thing about this business that you'd miss?", sites: [['The skill page', SITE + '/ready/?all=1#d7'], ["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: "sk8", g: "skills", ty: "live", k: "Skill 8", t: "Test your business name", p: "What AI hears when it hears it cold.", prompt: "I'm going to say a business name one time: [your business name]. What do you think this business does? How would you spell it? And what would you type to find it online?", sites: [['The skill page', SITE + '/ready/?all=1#d8'], ["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: "sk9", g: "skills", ty: "live", k: "Skill 9", t: "The thank-you that brings them back", p: "In your own words, in a minute.", prompt: "Write a short thank-you text to [first name]. We just [the job you did for them]. Mention [one real detail about it]. Ask for nothing. Make it sound like me, not a company.", sites: [['The skill page', SITE + '/ready/?all=1#d9'], ["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: "sk10", g: "skills", ty: "live", k: "Skill 10", t: "What one customer is worth", p: "The number nobody ran for you.", prompt: "Help me work out what one regular customer is worth to my business over a year. Ask me what you need to know, one question at a time.", sites: [['The skill page', SITE + '/ready/?all=1#d10'], ["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: "sk11", g: "skills", ty: "live", k: "Skill 11", t: "Ask AI who's the best near you", p: "Does it say your name?", sites: [['The skill page', SITE + '/ready/?all=1#d11'], ["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: "sk12", g: "skills", ty: "live", k: "Skill 12", t: "Get a read on anyone", p: "Start with your favorite star.", prompt: "From what's public, give me a read on [famous person]. What drives them? What do they want most? How do they make decisions? If I had five minutes with them, how would I win them over?", sites: [['The skill page', SITE + '/ready/?all=1#d12'], ["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: "explainer", g: "skills", ty: "live", k: "Skill", t: "Learn anything with an explainer video", p: "Pick one thing you always wanted to understand.", need: "Not in the twelve yet. Test which app makes a narrated video on a phone", prompt: "Make me a short explainer video that teaches me [one thing I've always wanted to understand]. Don't skimp on the audio: I want it narrated, start to finish.", sites: [["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: "metr", g: "smart", ty: "show", t: "How fast it's moving", p: "The length of job AI can finish on its own keeps doubling.", url: "https://metr.org/blog/2025-07-14-how-does-time-horizon-vary-across-domains", need: "Open the links once before the night; pick the chart that reads best on the big screen", note: "METR is a research group that measures how long a job AI can finish on its own, counted in how long it would take a skilled person. Their finding: that length has been doubling about every seven months since 2019, and faster lately (every three to four months, by 2026 reporting). The tasks they measure are software and research work, so say \"on the jobs they test.\" The point for the room: whatever it can do tonight, it does about twice as much a few months from now.", sites: [["METR's charts", "https://metr.org/blog/2025-07-14-how-does-time-horizon-vary-across-domains"], ["One simple chart (Dror Poleg)", "https://data.drorpoleg.com/charts/task-horizon/"], ["The original paper", "https://arxiv.org/html/2503.14499v1"]] },
  { id: "erdos80", g: "smart", ty: "show", t: "The 80-year math problem", p: "Open since 1946. AI cracked it in May.", url: "https://www.erdosproblems.com", need: "OpenAI's own post from May 20, 2026 (link not found yet); the news write-up is here meanwhile", note: "May 20, 2026: an OpenAI model overturned what the mathematician Paul Erd\u0151s guessed in 1946 about a geometry puzzle, something nobody had managed in 80 years. A Fields Medal winner (math's Nobel), Tim Gowers, called it a milestone and said he'd have accepted the paper. Plain version for the room: the best mathematicians alive couldn't crack it for 80 years, and AI did.", sites: [["News write-up", "https://noqta.tn/en/news/openai-reasoning-model-erdos-conjecture-math-breakthrough-2026"], ["The Erd\u0151s problems site", "https://www.erdosproblems.com"]] },
  { id: "liam", g: "smart", ty: "show", t: "The 23-year-old and one prompt", p: "A 60-year problem, 80 minutes, a ChatGPT account.", url: "https://www.scientificamerican.com/article/amateur-armed-with-chatgpt-vibe-maths-a-60-year-old-problem/", need: "Open the links once before the night to check they load", note: "April 2026: Liam Price, 23, no advanced math training, pasted Erd\u0151s problem #1196 into ChatGPT one Monday afternoon. About 80 minutes later it had an approach nobody had tried; Terence Tao and others checked it. He was on ChatGPT Pro, so don't say \"a $20 account.\" The line: \"One prompt. Like I'm about to show you how to do.\"", sites: [["Scientific American", "https://www.scientificamerican.com/article/amateur-armed-with-chatgpt-vibe-maths-a-60-year-old-problem/"], ["The problem itself", "https://www.erdosproblems.com/1196"]] },
  { id: "pile", g: "smart", ty: "show", k: "In just the last few years", t: "And that's just the start", p: "A Nobel Prize. A new antibiotic. Cancers caught early. A burned scroll read.", need: "A page to open for each one, if Jimmy wants to click through instead of saying them", note: "From the deck, one line each, fast: solved a 50-year biology puzzle and won a Nobel Prize (2024); found a new antibiotic that kills drug-resistant bacteria (MIT, 2020); caught 29% more breast cancers in a trial of 100,000 women (2025); read a scroll burned by Vesuvius 2,000 years ago without opening it; gave a man with ALS his own voice back (UC Davis, 2024); out-forecast the world's best weather system, hurricanes included (2024). The pile is the point." },
  { id: "adobe", g: "smart", ty: "show", t: "One guy vs. Adobe", p: "Seven Adobe apps rebuilt with AI in about a week. Free.", url: "https://getartcraft.com/apps", need: "Open the links once before the night to check they load", note: "How smart is it? Brandon Thomas, fed up with Adobe's subscription, used Claude to rebuild Photoshop, Illustrator, Premiere, Lightroom, After Effects, InDesign and Acrobat as free apps (ArtCraft). First code Sept 30, 2026; about eight days to all seven. A company with decades and thousands of engineers, matched in about a week, and now it's free. Say \"about a week,\" not \"a day.\" The apps are early and rough, so tell it as a story, not a demo of the app.", sites: [["ArtCraft apps", "https://getartcraft.com/apps"], ["The code", "https://github.com/storytold/artcraft"], ["Al Jazeera story", "https://www.aljazeera.com/news/2026/10/14/how-ai-apps-are-offering-free-substitutes-for-big-tech-software"]] },
  { id: 'prospect', g: 'sees', ty: 'live', t: 'Read a prospect before you call', p: 'Who they are, what they mean, how they see you.', need: 'One of Jimmy\'s real chamber or association reads as the backup',
    prompt: 'I\'m meeting [name], [title] at [business], today. Look them up. Tell me who they are, what they care about, how they\'ll probably read a message from me, what questions they\'ll have about me, and the best way to open the conversation.', sites: [["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: 'ian', g: 'sees', ty: 'show', t: 'Ian\'s business inside his business', p: 'A niche nobody owns. Now he leads it.', url: 'https://ineedjimmy.com/ianb/', need: 'Ian\'s niche and his live site' },
  { id: 'mccray', g: 'plate', ty: 'show', t: 'Dr. McCray\'s morning numbers', p: 'Every number he needs, every morning.', url: 'https://daegansmith.me/dr-mccray/', need: 'McCray\'s dashboard, a version safe for the big screen' },
  { id: 'maestro', g: 'plate', ty: 'show', t: 'Call the pizza shop', p: 'The AI answers and takes the order.', url: SITE + '/stories/maestros/', need: 'The phone number for the call' },
  { id: 'followup', g: 'plate', ty: 'show', t: 'Jamon\'s follow-up', p: 'From nothing to thank-you, review and referral.', url: SITE + '/stories/gotta-call-jack/', need: 'The messages themselves' },
  { id: 'ads', g: 'money', ty: 'show', t: 'Jamon\'s TV and radio ads', p: '$15,000 a month to over $50,000.', need: 'The ad files or links' },
  { id: 'jamonvid', g: 'money', ty: 'show', t: 'Jamon, in his own words', p: 'The video.', url: SITE + '/assets/jamon-testimonial.mp4' },
  { id: 'bread', g: 'money', ty: 'show', t: 'Jim\'s Amazing Bread', p: 'From losing money on every box.', url: 'https://jimsamazingbread.com', need: 'Jim\'s bread video' },
  { id: "jimmission", g: "money", ty: "show", t: "Jim: from bread to changing lives", p: "His why, then partners who serve the same people.", url: "https://jimsamazingbread.com", need: "The link to Lili's video and Jim's reviews page", note: "From the deck (Belief 4). When his daughter Lili started kindergarten, all her hair fell out in two weeks: Lyme disease and Epstein-Barr. A clinic in Florida put her on a gluten-free, dairy-free diet, and Jim made the bread so she'd have something she enjoyed eating. \"This is the only bread I can eat after 20 years.\" (JB, Crohn's patient.) The turn: he isn't selling bread, he's changing lives. That opens partners who sell to the same healthy-living customers (water filters, supplements, yoga): my customers become yours, yours become mine.", sites: [["Jim's Amazing Bread", "https://jimsamazingbread.com"]] },
  { id: 'estimate', g: 'money', ty: 'live', t: 'Jamon\'s estimate', p: 'One price becomes three.',
    prompt: 'Here\'s an estimate I gave for a job: a fence. Labor, materials, removal, permits. Total $7,000. Turn this into three options for the same job, good, better and best, with what\'s in each one and a price for each.', sites: [["Claude","https://claude.ai"],["ChatGPT","https://chatgpt.com"]] },
  { id: "jackname", g: "shows", ty: "show", t: "How we found GottaCallJack", p: "Not magic. We noticed the thing.", url: "https://gottacalljack.com", need: "The four screenshots: the chat, Namecheap, the ranking, the pick", note: "From the deck (Belief 6, second bite). His domain was TJOAT.net; nobody can say that. 1 Brainstorm names with AI. 2 Check what's available on Namecheap; most good ones are taken. 3 Have AI rank the ones that are left. 4 Choose the best one yourself, not the AI's pick. GottaCallJack.com: the action you want, his name, and the business. About nine bucks.", sites: [["GottaCallJack.com", "https://gottacalljack.com"], ["Namecheap", "https://www.namecheap.com"], ["Claude", "https://claude.ai"]] },
  { id: 'bruce', g: 'shows', ty: 'show', t: 'Bruce: a site with a personality', p: 'It feels like him.', url: 'https://ineedjimmy.com/bruce/', need: 'How Jimmy got Bruce\'s personality in' },
  { id: 'jack', g: 'shows', ty: 'show', t: 'TJOAT.net to GottaCallJack.com', p: 'Only how it shows up changed.', url: 'https://gottacalljack.com' },
  { id: 'wall', g: 'shows', ty: 'show', t: 'Neither were these', p: 'Lawyer, vape shop, photographer, DJ.', url: 'https://daegansmith.me/before-after.html' },
  { id: 'house', g: 'too', ty: 'show', t: 'Run your house from anywhere', p: 'Lights, TV, all by voice. You can too.', need: "Jimmy's Home Assistant steps (not found in this project's chats), then a clip or a live command",
    note: 'Quick aside, then "now, back with me." Keep moving.' },
  { id: 'research', g: 'yours', ty: 'live', t: 'What\'s great about your site', p: 'What\'s cool, and what\'s hiding.',
    prompt: 'Here\'s a local business website: [URL]. What would a customer want to find that isn\'t there? What does this business do well that the site never says? Give me the three changes that would bring in the most calls.', sites: [["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: 'loves', g: 'yours', ty: 'live', t: 'What your customers love', p: 'What they say that you never do.',
    prompt: 'Read the reviews and the website for [business, town]. What do customers love about them that the business never says anywhere? Quote the customers.', sites: [["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: 'newlook', g: 'yours', ty: 'live', bg: true, t: 'A new look', p: 'Their home page, redesigned while we talk.', need: 'Practice run: how long it takes',
    prompt: 'Here\'s [business]\'s website: [URL]. Redesign their home page so it\'s the best-looking one in [town] for what they do. Keep their real name, phone number, photos and reviews. Lead with what customers love about them. Build it as one page I can open in a browser.', sites: [["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: 'numbers', g: 'yours', ty: 'live', t: 'Your numbers', p: 'Where the money comes and goes.',
    prompt: 'I run [business]. Ask me five quick questions about my numbers, one at a time: what I charge, what it costs me, how many customers I get a month, how many come back, and where they come from. Then show me where I\'m making and losing money, and the one number to watch every morning.', sites: [["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: 'customers', g: 'yours', ty: 'live', bg: true, t: 'More customers', p: 'Ways to bring in more, fast.',
    prompt: 'I run [business] in [town]. Give me ten ways to get more customers in the next 30 days that cost little or nothing, ranked by how fast they\'d bring in money. For the top three, write exactly what I\'d say or post.', sites: [["Claude", "https://claude.ai"], ["ChatGPT", "https://chatgpt.com"]] },
  { id: 'offer', g: 'close', ty: 'show', k: 'The offer', t: 'The offer', p: 'The Build or the Meeting.', need: 'Offer v12 slides onto the board' },
  { id: 'orderform', g: 'close', ty: 'show', k: 'The offer', t: 'The order form', p: 'Paper, handed out. Fill it out quick.', url: SITE + '/print/enrollment-form.pdf' },
  { id: 'orderpage', g: 'close', ty: 'show', k: 'The offer', t: 'The order page', p: 'For anyone who\'d rather tap.', url: SITE + '/order/' }
];
