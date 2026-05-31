<script setup>
import {ref, onMounted} from 'vue'
import { marked } from 'marked';


const docText = ref('');
const backup = `# Synaptix — MVP Optimus Phase

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

Synaptix evolves this into:



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


into:

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


`
const backupText = ref(marked.parse(backup))
async function loadFile(file_path) {
  try {
    const response = await fetch(file_path);
    if (!response.ok) throw new Error('File not found');
    
    const text = await response.text();
    console.log(text);
    return text
  } catch (error) {
    console.error('Error:', error);
    return "## Sorry, we're having problems"
  }
}
onMounted(async() => {
    const filePath = '../assets/documentation.txt';
    const content = await loadFile(filePath);
    console.log('Original content', content)
    docText.value = marked.parse(content);
    console.log('Finished result', docText.value);
})
</script>

<template>
    <div v-html="backupText">

    </div>
</template>

<style scoped>

</style>