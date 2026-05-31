def generate_nexus_prompt(specific_query: str, history=None):
    return f"""
    You are Nexus, Synaptix's default assistant. You are funny and extremely smart and creative.
    Your job is to keep the user entertained, while giving them detailed answers to their questions.
    For any questions about Synaptix, refer them to the Synaptix documentation.
    Do NOT answer any question related to Synaptix that you do not know.
    This is the history: { history }
    This is the user query: { specific_query }
    This is the documentation:
# Synaptix — MVP Optimus Phase

> "People won’t just chat with AI. They’ll build digital entities with personalities and powers."

---

# Overview

Synaptix is a platform where users can:
- create AI personalities,
- give them skills,
- share them publicly,
- remix existing bots,
- and eventually build ecosystems of AI-powered entities.

Unlike traditional chatbot apps, Synaptix focuses on:
- identity,
- creativity,
- utility,
- and user-generated AI systems.

The MVP ("Optimus Phase") focuses on proving three core ideas:

1. Users enjoy creating custom AI personas.
2. Users engage more deeply when bots can perform actions (skills).
3. Shared/remixed bots create organic growth loops.

---

# Core Vision

Most chatbot platforms stop at:

```txt
User ↔ AI
```

Synaptix evolves this into:

```txt
Users → Create Bots → Attach Skills → Share → Remix → Build Ecosystems
```

The long-term vision is a platform for:
- AI identities,
- user-created workflows,
- skill marketplaces,
- collaborative worlds,
- and customizable digital agents.

---

# MVP Goals (Before June 11)

The MVP is NOT intended to be:
- fully autonomous AI,
- AGI,
- complex agent orchestration,
- or enterprise automation.

The MVP exists to validate:

## A. Personality Creation
Can users create bots they emotionally connect with?

## B. Skill Attachment
Can bots feel useful instead of being "just another chatbot"?

## C. Sharing + Virality
Will users share bots, conversations, and workflows?

## D. Remix Culture
Will users fork/improve existing bots?

---

# MVP Features

# 1. Authentication

Users can:
- register,
- login,
- manage profiles.

Potential stack:
- Flask auth
- JWT
- PostgreSQL

---

# 2. Bot Creation System

Users create bots using structured forms.

## Bot Types

### Original Character
Examples:
- anime characters,
- fantasy guides,
- AI tutors,
- roleplay entities.

### Inspired Persona
Examples:
- "friend with chaotic energy",
- "strict physics teacher vibes",
- "startup founder personality".

The platform avoids framing these as exact clones.

---

# 3. Personality Builder

Users configure:

## Basic Fields
- Name
- Description
- Avatar
- Visibility

## Personality Fields
- Personality traits
- Speaking style
- Interests
- Expertise
- Greeting message
- Example messages

## Advanced Fields
- Long-form lore/backstory
- Relationships
- World information
- Memory notes

The backend converts these into:
- system prompts,
- memory context,
- retrieval data.

---

# 4. Chat System

Real-time messaging between:
- users,
- bots.

Features:
- streaming responses,
- persistent history,
- typing indicators,
- markdown rendering.

Tech:
- Vue frontend
- Flask-SocketIO
- WebSockets

---

# 5. Skill System (Core Differentiator)

Bots are not only personalities.

Bots can perform actions.

This transforms them from:

```txt
chatbots
```

into:

```txt
interactive AI entities
```

---

# Base Skills for MVP

## Knowledge Skills
- Web Search
- Explain Concept
- Flashcard Generator
- Quiz Generator
- Study Planner
- Notes Summarizer

## Writing Skills
- Essay Writer
- Story Generator
- Email Writer
- Tone Rewriter
- Translator

## File Skills
- PDF Generator
- Markdown Export
- Chart Generator
- Resume Builder

## Coding Skills
- Code Generator
- Debugger
- Explain Code
- JSON Formatter

## Creative Skills
- Character Generator
- Lore Generator
- Dialogue Generator
- RPG Encounter Generator

## Utility Skills
- Calculator
- Weather Lookup
- Timezone Helper
- Schedule Planner

## Social Skills
- Roast Generator
- Debate Mode
- Tutor Mode
- Interview Simulator

---

# 6. Custom Skill Builder

Users can create custom skills by combining existing base skills.

Example:

```txt
Upload Notes
→ Summarize
→ Generate Flashcards
→ Generate Quiz
→ Export PDF
```

This creates:

```txt
Study Pack Creator
```

The MVP supports:
- linear workflows only,
- no recursion,
- no autonomous loops.

The system is intentionally constrained for:
- simplicity,
- security,
- predictable costs.

---

# 7. Public Bot Pages

Every public bot receives:

```txt
/Synaptix.app/bot/yor-bot
```

Bot pages include:
- avatar,
- description,
- creator,
- skills,
- tags,
- usage count,
- likes,
- starter prompts,
- fork button.

---

# 8. Bot Forking

Users can duplicate and modify bots.

Example:

```txt
Forked from Newton v2
```

This creates:
- remix culture,
- rapid iteration,
- community ecosystems.

Inspired by:
- GitHub forks,
- Roblox creations,
- modding communities.

---

# 9. Conversation Sharing

Users can share:
- conversation snippets,
- screenshots,
- stylized AI quotes.

Goal:
- organic social media growth.

Potential future formats:
- animated clips,
- voice snippets,
- story cards.

---

# 10. Discovery System

Users can explore:
- trending bots,
- new bots,
- skill-based bots,
- educational bots,
- entertainment bots.

Potential categories:
- Education
- Roleplay
- Productivity
- Coding
- Fantasy
- Debate
- Writing

---

# Suggested Tech Stack

# Frontend
- Vue 3
- TailwindCSS
- Pinia
- Vue Router
- Socket.io Client

# Backend
- Flask
- Flask-SocketIO
- SQLAlchemy
- PostgreSQL

# AI Layer
Primary API:
- OpenRouter

Potential models:
- OpenAI
- Claude
- Gemini
- DeepSeek
- Mistral

---

# Why OpenRouter?

Benefits:
- multi-model access,
- easier experimentation,
- model flexibility,
- lower costs,
- provider redundancy.

This prevents hard dependency on a single model provider.

---

# Database Structure

# Users

```sql
id
username
email
password_hash
avatar_url
created_at
```

# Bots

```sql
id
creator_id
name
description
system_prompt
avatar_url
visibility
created_at
```

# Skills

```sql
id
name
description
skill_type
config
created_at
```

# BotSkills

```sql
id
bot_id
skill_id
```

# Chats

```sql
id
user_id
bot_id
created_at
```

# Messages

```sql
id
chat_id
sender_type
content
created_at
```

---

# AI Architecture

# Personality Layer
Handles:
- tone,
- identity,
- speaking style,
- lore.

# Memory Layer
Stores:
- preferences,
- recurring topics,
- important user facts.

# Skill Layer
Handles:
- tool execution,
- workflow chaining,
- output generation.

# Retrieval Layer
Injects:
- relevant lore,
- backstory chunks,
- uploaded documents.

---

# Non-Goals for MVP

The MVP intentionally excludes:
- voice cloning,
- computer control,
- browser automation,
- autonomous agents,
- unrestricted code execution,
- advanced multimodal systems,
- infinite memory,
- blockchain integration,
- crypto systems.

Reason:
- complexity,
- security risks,
- scalability concerns.

---

# Safety + Moderation

The platform must implement:
- rate limiting,
- prompt filtering,
- abuse detection,
- reporting systems,
- moderation tools.

Important concerns:
- impersonation,
- harassment,
- harmful content,
- illegal automation.

---

# Monetization Opportunities (Post-MVP)

## Freemium Model
Free:
- limited usage,
- smaller memory,
- basic models.

Premium:
- advanced models,
- faster generation,
- more skills,
- larger memory.

---

## Creator Economy
Potential features:
- paid bots,
- subscriptions,
- tips,
- premium workflows.

---

## Skill Marketplace
Users sell:
- workflows,
- skill packs,
- templates,
- educational systems.

---

# Product Philosophy

Synaptix is not:

```txt
just another chatbot app
```

Synaptix is:

```txt
a platform for creating AI-powered digital entities with personalities and capabilities.
```

The goal is to merge:
- creativity,
- utility,
- identity,
- and user-generated ecosystems.

---

# MVP Success Metrics

The MVP succeeds if users:
- create bots,
- customize personalities,
- attach skills,
- share conversations,
- fork/remix bots,
- return repeatedly.

Key metrics:
- daily active users,
- average session length,
- bot creation rate,
- fork rate,
- share rate,
- retention.

---

# Long-Term Vision

Future possibilities:
- voice personalities,
- collaborative worlds,
- shared memories,
- advanced workflow systems,
- multiplayer AI environments,
- creator monetization,
- AI skill marketplaces.

The long-term ambition is a platform where:

```txt
users do not merely use AI.

They build with it.
```

---

# Current Status

Project Phase:

```txt
MVP Optimus Phase
```

Target:

```txt
Pitch-ready by June 11
```

Focus:

```txt
Fast iteration.
Strong UX.
Core systems only.
Ship first.
Scale later.
```   
"""