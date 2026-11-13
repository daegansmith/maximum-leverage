# Make It Simple

Sometimes Claude gives me way too much. I only want two things: what do I have to do, and are we done?

<img class="arcimg" src="arc.png" alt="A line that starts low when Claude tells me everything and climbs to done when I say make it simple.">

## The Problem

We talk about a lot of things. Then the answer comes back with "and this, and this, and here are the things to think about." Most of it will not change what I do. Reading it is a waste of my time.

I do not need all of that. I need to get the thing done.

<img class="frame" src="f1.png" alt="Claude hands me a pile of everything and I look unhappy.">

## The Fix

I made a skill called make-it-simple. When I say "make it simple," Claude throws out everything that does not matter and gives me this:

1. Done, or not done yet.
2. The few things only I have to do, as 1, 2, 3.
3. Nothing else.

It talks like I am in third grade. Short words. Short sentences.

<img class="frame" src="f2.png" alt="I say make it simple and it goes into a box.">

<img class="frame" src="f3.png" alt="What comes out is a page that says 1 2 3.">

## What It Never Cuts

If skipping something would cost me money or break the result, it stays. It gets one line, right at the step it touches. Everything else goes.

## Before And After

**Before:** Four paragraphs on how the website move works, three options for the domain, and a list of things to consider about email.

**After:**

Not done yet.

1. Log in to GoDaddy.
2. Click "Forwarding" and paste the new link.
3. Tell me when it is saved.

<img class="frame" src="f4.png" alt="I do the steps and it says done.">

## Why Not Just Make An Explainer Video

I do that too, for big new topics. It works. It also costs a lot of effort. Most days I do not need a video. I need three steps. This takes a few seconds.

## Make Your Own

Anyone who works with Claude runs into this. Most people just wade through the extra. You do not have to. Tell Claude: "Make me a skill from this," then paste the text below.

    ---
    name: make-it-simple
    description: Cut any answer down to what I must do and whether it is done. Use when I say "make it simple", "too much", "just tell me what to do", or "are we done?".
    ---

    # Make It Simple

    I want two things: what do I have to do, and are we done?

    1. Start with one line: Done, or Not done yet. If I asked "will this work?", start with Yes or No.
    2. Then list only the things I have to do, as 1, 2, 3. One short sentence each, starting with a verb. If there is nothing, say "Nothing for you to do."
    3. Then stop.

    Cut anything that will not change what I do or whether it gets done. Make small decisions yourself. Skip how it works unless I ask. Do not list things you will handle as steps for me.

    Never cut anything that would cost me money or break the result. Give it one line, at the step it touches.

    Write like I am in third grade. Short words. Short sentences. No jargon.
