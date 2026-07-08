# Chapter 01 — JavaScript Engine

> "Before you can understand how JavaScript behaves, you need to understand who executes it."

---

# Chapter Overview

The JavaScript Engine is the heart of every JavaScript application.

Whether you're building an Angular application, a React application, or running JavaScript in Node.js, every line of JavaScript you write is ultimately executed by a JavaScript engine.

Most developers know **how to write JavaScript**, but very few understand **how JavaScript is actually executed**.

Understanding the JavaScript engine will help you understand many advanced topics, including:

- Execution Context
- Call Stack
- Memory Management
- Hoisting
- Scope
- Closures
- Event Loop
- Garbage Collection
- Performance Optimization
- Angular Change Detection (later chapters)

By the end of this chapter, you'll understand how your JavaScript code travels from a text file to machine instructions executed by the CPU.

---

# Learning Objectives

After completing this chapter, you should be able to:

- Explain what a JavaScript Engine is.
- Explain why JavaScript needs an engine.
- Differentiate JavaScript from the JavaScript Engine.
- Identify popular JavaScript engines.
- Understand the high-level architecture of the V8 engine.
- Explain the lifecycle of JavaScript code.
- Understand parsing and compilation at a high level.
- Explain why Angular developers should understand JavaScript internals.
- Answer JavaScript Engine interview questions confidently.

---

# Prerequisites

Before reading this chapter, you should know:

- Basic programming concepts
- Variables
- Functions (basic understanding)
- What a browser is

No advanced JavaScript knowledge is required.

---

# Chapter Roadmap

## Section 1 — Introduction to the JavaScript Engine

What is a JavaScript Engine?

---

---

# Section 2 — Why JavaScript Needs a JavaScript Engine

> *"JavaScript is a language. A language cannot execute itself. It always needs an engine to understand and execute it."*

---

## Learning Objectives

After completing this section, you will be able to:

- Explain why JavaScript requires a JavaScript Engine.
- Understand why CPUs cannot execute JavaScript directly.
- Describe the responsibilities of a JavaScript Engine.
- Explain how JavaScript code travels from a source file to the CPU.
- Answer interview questions related to JavaScript Engines confidently.

---

# Introduction

Suppose you write the following JavaScript code.

```javascript
console.log("Hello Angular Bootcamp!");
```

You save the file.

You open it in Chrome.

The message appears instantly in the browser console.

At first glance, it feels like magic.

But behind the scenes, several complex operations happen before you ever see the output.

Questions naturally arise:

- Who reads your JavaScript file?
- Who checks if your syntax is valid?
- Who allocates memory for variables?
- Who converts JavaScript into instructions the computer understands?
- Who finally executes the code?

The answer is:

> **The JavaScript Engine.**

Without a JavaScript Engine, JavaScript is nothing more than plain text stored inside a file.

---

# The Fundamental Problem

Computers do not understand JavaScript.

In fact, computers do not understand **any** high-level programming language.

A CPU understands only **machine instructions**.

Machine instructions look something like this:

```text
10110000
11000011
00101010
11100110
```

Writing software directly in binary would be almost impossible for humans.

Instead, we write programs using high-level languages such as:

- JavaScript
- TypeScript
- Java
- Python
- C#
- Go

These languages are designed for humans.

The CPU, however, cannot understand them.

This creates a gap between what humans write and what computers execute.

```text
Human
   │
   ▼
JavaScript Source Code
   │
   ▼
❌ CPU Cannot Understand This
   │
   ▼
Machine Instructions
   │
   ▼
CPU Executes
```

Someone has to bridge this gap.

That "someone" is the JavaScript Engine.

---

# The Role of the JavaScript Engine

Think of the JavaScript Engine as a translator between two worlds.

One world speaks JavaScript.

The other understands only machine instructions.

```
Developer
     │
     ▼
JavaScript Source Code
     │
     ▼
JavaScript Engine
     │
     ▼
Machine Instructions
     │
     ▼
CPU
```

The engine converts your human-readable JavaScript into instructions that the processor can execute.

However, translation is only one part of its job.

Modern JavaScript Engines perform many sophisticated tasks before your code ever runs.

---

# Responsibilities of a JavaScript Engine

A JavaScript Engine is responsible for much more than simply executing code.

Its major responsibilities include:

## 1. Reading Source Code

The engine first loads your JavaScript source file.

```javascript
const framework = "Angular";
```

At this point, it is simply plain text.

---

## 2. Parsing the Code

The engine analyzes the syntax of your program.

If your code contains an error such as:

```javascript
const name = ;
```

execution never begins.

Instead, the parser reports a syntax error.

---

## 3. Creating an Internal Representation

Once the syntax is valid, the engine converts your code into an internal representation.

Later in this chapter, we'll study:

- Tokens
- Lexical Analysis
- Abstract Syntax Tree (AST)

These structures help the engine understand the meaning of your code.

---

## 4. Allocating Memory

Before execution starts, memory is prepared for:

- Variables
- Functions
- Objects
- Classes

Example:

```javascript
let username = "Manish";

function greet() {
    console.log(username);
}
```

The engine prepares memory so these identifiers can be accessed during execution.

---

## 5. Executing the Program

Only after the previous stages are complete does execution begin.

```javascript
console.log("Hello");
console.log("World");
```

Output:

```text
Hello
World
```

---

## 6. Optimizing Performance

Modern engines continuously monitor your program.

If a particular function executes thousands of times, the engine may optimize it automatically.

This is one reason JavaScript performance has improved dramatically over the years.

We'll study these optimizations later when we explore the V8 engine.

---

## 7. Memory Cleanup

As your application runs, objects and variables become unnecessary.

The JavaScript Engine automatically frees unused memory using **Garbage Collection**.

Without this feature, applications would continuously consume memory until they crashed.

---

# Complete Journey of JavaScript Code

The complete lifecycle looks like this:

```text
Developer
    │
    ▼
Writes JavaScript Code
    │
    ▼
JavaScript Engine
    │
    ├── Reads Source Code
    ├── Parses the Code
    ├── Checks Syntax
    ├── Creates Internal Structures
    ├── Allocates Memory
    ├── Executes Code
    ├── Optimizes Frequently Used Code
    └── Cleans Unused Memory
    │
    ▼
Machine Instructions
    │
    ▼
CPU Executes Instructions
    │
    ▼
Program Output
```

This diagram summarizes everything we've discussed so far.

Each stage will be explored in detail in upcoming sections.

---

# Real-World Example

Consider the following Angular component:

```typescript
@Component({
  selector: 'app-user',
  template: `<button (click)="greet()">Click</button>`
})
export class UserComponent {

  name = "Manish";

  greet() {
    console.log(this.name);
  }

}
```

When you click the button:

1. Angular receives the click event.
2. Angular calls the `greet()` method.
3. The method has already been transpiled into JavaScript.
4. The JavaScript Engine executes the generated JavaScript.
5. The browser displays the output.

Angular never executes your code directly.

The JavaScript Engine does.

This is why understanding the engine helps you understand Angular itself.

---

# Common Misconceptions

### ❌ JavaScript executes itself.

No.

A JavaScript Engine executes JavaScript.

---

### ❌ Browsers understand JavaScript natively.

Not exactly.

Browsers embed a JavaScript Engine that understands JavaScript.

---

### ❌ The JavaScript Engine only translates code.

Incorrect.

Modern engines:

- Parse code
- Analyze syntax
- Allocate memory
- Optimize execution
- Execute instructions
- Perform Garbage Collection

Translation is only one part of the process.

---

# Interview Perspective

### Question

**Why does JavaScript need a JavaScript Engine?**

A beginner might answer:

> "Because JavaScript needs something to execute it."

A stronger answer would be:

> "JavaScript is a high-level programming language designed for humans, while CPUs execute only machine instructions. A JavaScript Engine bridges this gap by parsing JavaScript, validating its syntax, creating internal representations, allocating memory, optimizing frequently executed code, executing instructions, and reclaiming unused memory through garbage collection."

Notice that this answer explains both **what** the engine does and **why** it exists.

---

# Key Takeaways

- JavaScript is a high-level programming language.
- CPUs cannot execute JavaScript directly.
- A JavaScript Engine converts JavaScript into executable instructions.
- Modern JavaScript Engines perform parsing, memory management, optimization, execution, and garbage collection.
- Every Angular application ultimately runs because a JavaScript Engine executes the generated JavaScript.

---

## Next Section

In **Section 3**, we'll explore **Browser Architecture** and answer an important question:

> **Where does the JavaScript Engine actually live inside the browser, and what other browser components work alongside it?**

---

---

# Section 3 — Browser Architecture

> *"Before understanding where the JavaScript Engine lives, we must first understand how a modern browser is designed."*

---

## Learning Objectives

By the end of this section, you will be able to:

- Understand what a browser actually is.
- Identify the major components of a modern browser.
- Explain the responsibilities of each browser process.
- Understand where the JavaScript Engine lives.
- Explain why browsers use multiple processes.
- Connect browser architecture with Angular applications.

---

# Introduction

Most developers think of a browser as a simple application that displays websites.

When you open Google Chrome, Microsoft Edge, Firefox, or Safari, it feels like a single program.

In reality, a browser is an extremely complex piece of software consisting of multiple independent processes working together.

Each process has a specific responsibility.

This architecture allows browsers to remain:

- Fast
- Secure
- Stable
- Responsive

Understanding browser architecture is important because your Angular application spends its entire life inside one of these browser processes.

---

# What Happens When You Open a Website?

Suppose you visit:

```
https://angular.dev
```

The sequence is much more complicated than simply downloading HTML.

A simplified version looks like this:

```text
You Enter URL
        │
        ▼
Browser Receives Request
        │
        ▼
DNS Lookup
        │
        ▼
HTTP/HTTPS Request
        │
        ▼
Server Returns Response
        │
        ▼
Browser Starts Rendering
        │
        ▼
HTML Parsing
        │
        ▼
CSS Parsing
        │
        ▼
JavaScript Execution
        │
        ▼
DOM Construction
        │
        ▼
Page Rendering
```

Every one of these steps involves different browser components working together.

---

# Browser Architecture Overview

A modern Chromium-based browser (such as Chrome or Edge) is divided into multiple processes.

```text
                Browser

                    │

     ┌──────────────┼──────────────┐
     │              │              │
     ▼              ▼              ▼

Browser Process  Renderer      GPU Process
                  Process

                    │

        ┌───────────┼────────────┐
        │           │            │

        ▼           ▼            ▼

HTML Parser   CSS Engine   JavaScript Engine

                    │

                    ▼

            Rendering Engine
```

This diagram is simplified, but it gives a good mental model.

---

# Browser Process

The Browser Process acts as the coordinator.

It is responsible for managing the browser itself.

Responsibilities include:

- Opening and closing tabs
- Address bar
- Navigation
- Bookmarks
- Downloads
- Browser history
- Permissions
- Cookies
- Communication with other processes

Think of it as the "manager" of the browser.

It does **not** execute your Angular application.

---

# Renderer Process

The Renderer Process is the most important process for frontend developers.

Every web page is rendered inside a renderer process.

Its responsibilities include:

- Parsing HTML
- Parsing CSS
- Building the DOM
- Executing JavaScript
- Calculating layouts
- Painting pixels
- Handling user interactions

This is where your Angular application lives.

Everything you write in Angular eventually executes inside the Renderer Process.

---

# Inside the Renderer Process

The Renderer Process itself contains several important subsystems.

```text
Renderer Process

├── HTML Parser
├── CSS Engine
├── JavaScript Engine
├── DOM
├── Rendering Engine
├── Layout Engine
└── Paint System
```

Each subsystem has a dedicated responsibility.

For example:

- HTML Parser builds the DOM.
- CSS Engine calculates styles.
- JavaScript Engine executes your JavaScript.
- Rendering Engine paints the page.

---

# GPU Process

Modern browsers also include a dedicated GPU Process.

Its job is to:

- Render animations
- Accelerate graphics
- Draw complex visual effects
- Improve scrolling performance
- Handle compositing

This keeps rendering smooth even when the CPU is busy.

---

# Network Process

The Network Process handles communication with servers.

Responsibilities include:

- HTTP requests
- HTTPS requests
- WebSocket connections
- DNS lookups
- SSL/TLS
- Downloading images
- Downloading JavaScript bundles
- Downloading CSS files

Whenever your Angular application calls:

```typescript
this.http.get(...)
```

the browser's networking infrastructure is ultimately responsible for sending that request.

---

# Storage

Modern browsers also manage persistent storage.

Examples include:

- Cookies
- localStorage
- sessionStorage
- IndexedDB
- Cache Storage

These APIs are provided by the browser—not by JavaScript itself.

---

# Where Does the JavaScript Engine Live?

This is one of the most common interview questions.

The JavaScript Engine is located inside the **Renderer Process**.

```text
Browser

└── Renderer Process

        ├── HTML Parser

        ├── CSS Engine

        ├── JavaScript Engine

        ├── DOM

        └── Rendering Engine
```

The engine is responsible only for executing JavaScript.

It does **not**:

- Draw the screen
- Build the DOM
- Download resources
- Paint pixels

Those tasks belong to other browser components.

---

# Why Multiple Processes?

Older browsers often used a single process.

This created several problems.

If one tab crashed,

the entire browser crashed.

Modern browsers isolate work into separate processes.

Benefits include:

## Stability

If one tab crashes,

other tabs continue running.

---

## Security

Each renderer process runs inside a sandbox.

This limits the damage malicious websites can cause.

---

## Performance

Different browser components can work simultaneously.

For example:

- Downloading files
- Executing JavaScript
- Rendering animations

can all happen independently.

---

# Angular Connection

When an Angular application starts:

1. The Network Process downloads your bundled JavaScript.
2. The Renderer Process parses HTML.
3. CSS is processed.
4. The JavaScript Engine executes Angular.
5. Angular creates components.
6. Angular updates the DOM.
7. The Rendering Engine paints the UI.

Understanding this flow helps explain why large bundles, heavy JavaScript execution, or expensive rendering can slow down an Angular application.

---

# Interview Perspective

### Question

**Where does JavaScript actually execute inside the browser?**

Incorrect answer:

> Inside Chrome.

Better answer:

> JavaScript executes inside the JavaScript Engine, which runs within the browser's Renderer Process. The Renderer Process also handles HTML parsing, CSS processing, DOM creation, layout, and rendering.

---

### Question

**Does the JavaScript Engine build the DOM?**

Answer:

No.

The HTML Parser constructs the DOM.

The JavaScript Engine interacts with the DOM through Browser APIs.

---

# Common Mistakes

❌ Thinking the browser is a single process.

❌ Believing JavaScript builds the DOM.

❌ Assuming the JavaScript Engine performs rendering.

❌ Confusing Browser APIs with the JavaScript Engine.

❌ Assuming Angular controls browser rendering.

---

# Key Takeaways

- Modern browsers are multi-process applications.
- Your Angular application runs inside the Renderer Process.
- The JavaScript Engine is only one component of the Renderer Process.
- HTML parsing, CSS processing, rendering, networking, and storage are handled by different browser components.
- Understanding browser architecture helps explain application performance, debugging, and rendering behavior.

---

## Next Section

In **Section 4 — JavaScript Engine vs Browser APIs**, we'll answer another interview favorite:

> **"Is `setTimeout()` part of JavaScript?"**

You'll discover why many commonly used APIs are **not** actually part of the JavaScript language.

---

---

# Section 4 — JavaScript Engine vs Browser APIs

> *"One of the biggest misconceptions among JavaScript developers is believing that everything they use belongs to JavaScript."*

---

## Learning Objectives

By the end of this section, you will be able to:

- Differentiate between the JavaScript language and Browser APIs.
- Explain what the JavaScript Engine is responsible for.
- Identify APIs that are provided by the browser.
- Understand why JavaScript can run in different environments.
- Answer common interview questions about Browser APIs.

---

# Introduction

Consider the following code.

```javascript
console.log(window);
console.log(document);
console.log(localStorage);

setTimeout(() => {
    console.log("Hello");
}, 1000);

fetch("/users");
```

Most developers assume that everything above belongs to JavaScript.

Surprisingly, that's not true.

In reality, JavaScript itself knows nothing about:

- `window`
- `document`
- `fetch()`
- `setTimeout()`
- `localStorage`
- `alert()`
- `navigator`

These are **Browser APIs**.

The JavaScript Engine simply executes your JavaScript code.

The browser provides these APIs.

Understanding this distinction is essential because the same JavaScript language can run in multiple environments—not just browsers.

---

# JavaScript vs Browser

Think of JavaScript as a language specification.

It defines concepts such as:

- Variables
- Functions
- Objects
- Arrays
- Classes
- Promises
- Modules

It **does not** define:

- DOM
- HTML
- CSS
- Network requests
- Browser storage
- Timers

Those capabilities come from the environment hosting JavaScript.

---

# Browser APIs

A browser exposes additional functionality to JavaScript through APIs.

Some of the most commonly used Browser APIs include:

| Browser API | Purpose |
|-------------|---------|
| `window` | Represents the browser window |
| `document` | Accesses and manipulates the DOM |
| `fetch()` | Makes HTTP requests |
| `setTimeout()` | Schedules future execution |
| `setInterval()` | Executes repeatedly |
| `localStorage` | Stores persistent key-value data |
| `sessionStorage` | Stores session-based data |
| `navigator` | Provides browser information |
| `history` | Browser navigation |
| `location` | Current URL information |
| `WebSocket` | Real-time communication |
| `IndexedDB` | Client-side database |

These APIs are available because the browser provides them—not because JavaScript defines them.

---

# The Relationship

A simplified architecture looks like this:

```text
                Browser

        ┌───────────────────────┐
        │      Browser APIs      │
        │                       │
        │ window                │
        │ document              │
        │ fetch                 │
        │ localStorage          │
        │ setTimeout            │
        │ navigator             │
        └──────────┬────────────┘
                   │
                   ▼
          JavaScript Engine
                   │
                   ▼
          Executes JavaScript
```

Notice that the engine sits below the Browser APIs.

When your code calls:

```javascript
setTimeout(() => {
    console.log("Done");
}, 1000);
```

The flow is roughly:

1. JavaScript Engine encounters `setTimeout()`.
2. Browser receives the request.
3. Browser starts a timer.
4. Once the timer expires, the callback is queued.
5. The JavaScript Engine executes the callback when appropriate.

The timer itself is **not** managed by the JavaScript Engine.

---

# Another Runtime, Same JavaScript

Now consider Node.js.

```javascript
const fs = require("fs");

fs.readFile("data.txt", () => {
    console.log("Completed");
});
```

Here:

- There is no `window`.
- There is no `document`.
- There is no DOM.

Instead, Node.js provides:

- File System API
- Process API
- Buffer API
- Stream API

The JavaScript language remains the same.

Only the runtime APIs change.

This is why JavaScript is called a **hosted language**.

---

# Real-World Example

In Angular, we often write:

```typescript
localStorage.setItem("theme", "dark");
```

Angular does not provide `localStorage`.

The browser does.

Similarly:

```typescript
window.scrollTo(0, 0);
```

Again:

- Not Angular.
- Not JavaScript.
- Browser API.

Understanding this helps when building applications that also run in environments like server-side rendering, where some browser APIs may not exist.

---

# Angular Connection

Angular tries to reduce direct dependency on browser-specific APIs.

For example, instead of manipulating the DOM directly:

```typescript
document.getElementById("title").innerHTML = "Hello";
```

Angular encourages using templates, bindings, or abstractions like `Renderer2`.

Why?

Because browser APIs may not be available in every execution environment.

Keeping this separation improves portability and maintainability.

---

# Interview Perspective

### Question

**Is `setTimeout()` part of JavaScript?**

❌ Common Answer

> Yes.

✅ Correct Answer

No.

`setTimeout()` is a Browser API (or a runtime API in environments like Node.js). JavaScript simply invokes it.

---

### Question

**Who provides `document`?**

Correct Answer:

The browser provides the `document` object through the DOM API.

The JavaScript Engine only executes code that accesses it.

---

### Question

**Can JavaScript exist without the browser?**

Yes.

Examples include:

- Node.js
- Deno
- Bun

Each provides its own runtime APIs while executing the same JavaScript language.

---

# Common Mistakes

❌ Thinking every global object belongs to JavaScript.

❌ Assuming `fetch()` is part of ECMAScript.

❌ Believing the JavaScript Engine manages timers.

❌ Confusing Browser APIs with the JavaScript language.

❌ Assuming Angular provides browser objects.

---

# Key Takeaways

- JavaScript is a language specification.
- The JavaScript Engine executes JavaScript.
- The browser provides Browser APIs.
- Different runtimes expose different APIs.
- Angular applications depend on Browser APIs but do not create them.

---

## Next Section

In **Section 5 — Popular JavaScript Engines**, we'll explore the engines that power modern JavaScript environments, including:

- V8
- SpiderMonkey
- JavaScriptCore
- Chakra (historical)
- Why V8 became the industry standard
- Why Node.js also uses V8

---

---

# Section 5 — Popular JavaScript Engines

> *"JavaScript is one language, but it is executed by different engines depending on where it runs."*

---

## Learning Objectives

By the end of this section, you will be able to:

- Understand what a JavaScript Engine is.
- Identify the major JavaScript Engines used today.
- Explain why different browsers use different engines.
- Understand why Node.js uses V8.
- Explain why JavaScript behaves consistently across browsers.
- Answer common interview questions about JavaScript Engines.

---

# Introduction

By now, we know that JavaScript cannot execute itself.

It always needs a **JavaScript Engine**.

One question naturally follows.

> **If every browser executes JavaScript, do they all use the same engine?**

The answer is **No**.

Each browser vendor has built its own JavaScript Engine.

Although all engines execute JavaScript, they are implemented differently and optimized using different techniques.

Despite these differences, they all aim to follow the **ECMAScript Specification**, ensuring that the same JavaScript program behaves consistently across environments.

---

# Why Are There Multiple JavaScript Engines?

Imagine if every car manufacturer had to build the exact same engine.

Innovation would stop.

Instead, companies design their own engines while still following common standards.

The same idea applies to browsers.

The ECMAScript specification defines **how JavaScript should behave**, but it does **not** define **how a JavaScript Engine must be implemented**.

This allows browser vendors to innovate and compete on performance, memory usage, and optimization strategies.

---

# Major JavaScript Engines

Today, four JavaScript Engines are historically significant.

| JavaScript Engine | Developed By | Used In | Status |
|-------------------|--------------|---------|--------|
| **V8** | Google | Chrome, Edge, Node.js, Deno, Bun (uses JavaScriptCore-derived parser? no—Bun embeds JavaScriptCore) | Widely Used |
| **SpiderMonkey** | Mozilla | Firefox | Active |
| **JavaScriptCore** | Apple | Safari | Active |
| **Chakra** | Microsoft | Legacy Edge | Mostly Retired |

> **Note:** Modern Microsoft Edge no longer uses Chakra. Since moving to Chromium, it uses **V8**.

---

# V8

## Overview

V8 is Google's JavaScript Engine.

It was first released in **2008** as part of Google Chrome.

Its primary goal was simple:

> **Make JavaScript dramatically faster.**

Before V8, JavaScript execution was significantly slower because most engines relied heavily on interpretation.

V8 introduced aggressive optimization techniques that transformed JavaScript into a language capable of powering large-scale applications.

Today, V8 powers:

- Google Chrome
- Microsoft Edge
- Node.js
- Electron applications
- Many desktop applications
- Several server-side JavaScript runtimes

---

## Why Is V8 So Popular?

Several reasons contributed to V8's popularity.

### High Performance

V8 continuously analyzes running code and optimizes frequently executed functions.

This makes JavaScript significantly faster during long-running applications.

---

### Memory Management

V8 includes sophisticated Garbage Collection algorithms that automatically reclaim unused memory.

This reduces memory leaks and improves application stability.

---

### Open Source

Google made V8 open source.

This allowed other projects, including Node.js, to adopt it.

---

### Continuous Improvement

Every year, Google's V8 team introduces new optimizations.

Modern versions include multiple execution tiers that balance startup speed with runtime performance.

We'll explore these execution stages later in this chapter.

---

# SpiderMonkey

SpiderMonkey is Mozilla's JavaScript Engine.

It was the **first JavaScript Engine ever created**.

Originally developed by **Brendan Eich**, the creator of JavaScript, it powers Mozilla Firefox.

Like V8, SpiderMonkey implements the ECMAScript specification but uses its own internal architecture and optimization techniques.

---

# JavaScriptCore

JavaScriptCore is Apple's JavaScript Engine.

It powers:

- Safari
- WebKit-based browsers
- Many Apple platforms

JavaScriptCore focuses heavily on performance and energy efficiency, which is especially important for mobile devices.

---

# Chakra

Chakra was Microsoft's JavaScript Engine for the original Microsoft Edge browser.

After Microsoft adopted Chromium, Edge switched to V8.

Although Chakra is no longer the primary engine for Edge, it remains an important part of JavaScript history.

---

# One Language, Multiple Engines

Although different engines exist, developers usually do not need to write separate JavaScript for each browser.

Why?

Because every engine aims to follow the **ECMAScript Specification**.

Consider this code:

```javascript
const numbers = [10, 20, 30];

console.log(numbers.length);
```

Whether this runs in:

- Chrome
- Firefox
- Safari
- Node.js

the result is the same:

```text
3
```

The engines may execute the code differently internally, but the observable behavior should remain consistent.

---

# Why Doesn't Every Engine Work Exactly the Same Way?

The ECMAScript specification defines **behavior**, not **implementation**.

Think of it like an examination.

Every student receives the same questions.

Each student may solve them differently.

Similarly,

Every JavaScript Engine receives the same language specification.

Each engine is free to implement its own parser, optimizer, compiler, and memory management techniques.

This competition encourages innovation and improves JavaScript performance across the ecosystem.

---

# Which Engine Should Angular Developers Learn?

For most Angular developers, the answer is:

> **V8**

Why?

Because:

- Google Chrome is widely used for development.
- Microsoft Edge also uses V8.
- Angular CLI development commonly happens in Chromium-based browsers.
- Server-side rendering with Node.js also uses V8.

Understanding V8 provides knowledge that applies to both client-side and server-side Angular applications.

That said, remember that Angular itself is **not tied to V8**. An Angular application can also run in Firefox (SpiderMonkey) or Safari (JavaScriptCore), provided the browser supports the required web standards.

---

# Real-World Example

Imagine you're developing an Angular application.

During development:

```text
Angular Source Code
        │
        ▼
TypeScript Compiler
        │
        ▼
JavaScript Bundle
        │
        ▼
Chrome Browser
        │
        ▼
V8 Executes JavaScript
```

If the same application is opened in Firefox:

```text
Angular Source Code
        │
        ▼
JavaScript Bundle
        │
        ▼
Firefox Browser
        │
        ▼
SpiderMonkey Executes JavaScript
```

The application remains the same.

Only the JavaScript Engine changes.

---

# Interview Perspective

### Question

**Which JavaScript Engine does Google Chrome use?**

**Answer:**

V8.

---

### Question

**Which JavaScript Engine does Firefox use?**

**Answer:**

SpiderMonkey.

---

### Question

**Which JavaScript Engine does Safari use?**

**Answer:**

JavaScriptCore.

---

### Question

**Does Node.js have its own JavaScript Engine?**

**Answer:**

No.

Node.js embeds Google's **V8** engine and provides additional runtime APIs for server-side development.

---

### Question

**Why can the same JavaScript code run in different browsers?**

**Answer:**

Because modern JavaScript Engines implement the ECMAScript specification, ensuring consistent language behavior even though their internal implementations differ.

---

# Common Mistakes

❌ Thinking JavaScript has only one engine.

❌ Assuming Chrome created the JavaScript language.

❌ Believing Node.js has a unique JavaScript Engine.

❌ Confusing the ECMAScript specification with a JavaScript Engine.

❌ Assuming all engines use the same internal architecture.

---

# Key Takeaways

- JavaScript is one language but has multiple engine implementations.
- Different browsers use different JavaScript Engines.
- V8 powers Chrome, Edge, and Node.js.
- Firefox uses SpiderMonkey.
- Safari uses JavaScriptCore.
- All major engines implement the ECMAScript specification.
- Angular applications can run on any compliant JavaScript Engine.

---

## Next Section

In **Section 6 — Inside the V8 Engine**, we'll move beyond names and begin exploring the internal architecture of the world's most widely used JavaScript Engine.

We'll cover:

- V8 architecture
- Ignition Interpreter
- Sparkplug
- TurboFan
- Maglev
- Just-In-Time (JIT) Compilation
- Hidden Classes
- Inline Caching

This is where we start looking inside the engine itself.

---

---

# Section 6 — Inside the V8 Engine

> *"Knowing that Chrome uses V8 is useful. Understanding how V8 executes your code is what separates an experienced JavaScript developer from someone who only writes JavaScript."*

---

## Learning Objectives

After completing this section, you will be able to:

- Understand what V8 is.
- Explain why V8 is one of the fastest JavaScript engines.
- Identify the major components of the V8 architecture.
- Understand the role of the Parser, Ignition, Sparkplug, Maglev, and TurboFan.
- Explain the high-level execution pipeline.
- Understand how V8 improves JavaScript performance.

---

# Introduction

In the previous section, we learned that Chrome, Edge, and Node.js use **V8** to execute JavaScript.

Now the obvious question is:

> **What actually happens inside V8 when it receives a JavaScript file?**

Many developers imagine something simple.

```text
JavaScript
     │
     ▼
Execute
```

Reality is much more sophisticated.

Modern V8 performs several stages before your code reaches the CPU.

It reads your source code, validates it, converts it into internal structures, executes it, observes how it behaves, and continuously optimizes it while your application is running.

This optimization pipeline is one of the reasons JavaScript applications have become incredibly fast.

---

# What is V8?

V8 is Google's open-source JavaScript Engine.

It was first introduced in **2008** with Google Chrome.

Its primary objective was to make JavaScript fast enough for large, complex web applications.

Today, V8 powers:

- Google Chrome
- Microsoft Edge
- Node.js
- Electron
- Many desktop applications
- Numerous backend JavaScript services

Millions of JavaScript programs are executed by V8 every day.

---

# Why Was V8 Revolutionary?

Before V8, JavaScript engines mainly interpreted code.

As web applications became larger and more interactive, developers needed much better performance.

V8 introduced aggressive optimization strategies.

Instead of simply executing code line by line, it analyzes running programs, identifies frequently executed code, and optimizes it dynamically.

This approach dramatically improved JavaScript performance.

---

# High-Level Architecture of V8

At a high level, V8 processes JavaScript through several stages.

```text
JavaScript Source Code
          │
          ▼
      Parser
          │
          ▼
 Abstract Syntax Tree (AST)
          │
          ▼
 Ignition Interpreter
          │
          ▼
 Bytecode
          │
          ▼
  Sparkplug Compiler
          │
          ▼
  Maglev Compiler
          │
          ▼
 TurboFan Optimizing Compiler
          │
          ▼
 Optimized Machine Code
          │
          ▼
         CPU
```

Do not worry if some of these names are unfamiliar.

Each component has a specific responsibility, and we'll explore them in detail throughout this chapter.

---

# Step 1 — Parser

The first component that receives your JavaScript code is the **Parser**.

Suppose you write:

```javascript
function greet(name) {
    return `Hello ${name}`;
}

greet("Manish");
```

The parser checks:

- Is the syntax valid?
- Are brackets balanced?
- Are keywords used correctly?
- Can the program be understood?

If the parser detects invalid syntax, execution stops immediately.

Example:

```javascript
const user = ;
```

This code never executes because the parser reports a syntax error.

---

# Step 2 — Abstract Syntax Tree (AST)

After parsing succeeds, V8 converts the source code into an internal structure called the **Abstract Syntax Tree (AST)**.

Think of the AST as a blueprint of your program.

Instead of storing code as plain text, the engine represents it as interconnected nodes.

A simplified example:

```javascript
const age = 25;
```

becomes conceptually:

```text
VariableDeclaration
│
├── Identifier(age)
│
└── NumericLiteral(25)
```

This representation allows the engine to analyze and optimize your program efficiently.

We'll dedicate an entire section to AST later in this chapter.

---

# Step 3 — Ignition Interpreter

Once the AST is created, V8 passes it to **Ignition**.

Ignition is V8's interpreter.

Its job is to convert the AST into **bytecode** and begin execution as quickly as possible.

Why not generate highly optimized machine code immediately?

Because optimization takes time.

If a function runs only once, spending significant time optimizing it would actually slow down the application.

Ignition prioritizes fast startup.

---

# Step 4 — Sparkplug

Sparkplug is V8's baseline compiler.

It compiles bytecode into machine code very quickly.

Its goal is simple:

- Improve performance.
- Keep compilation overhead low.

Sparkplug acts as an intermediate step before more advanced optimizations.

---

# Step 5 — Maglev

Maglev is a newer optimizing compiler designed to bridge the gap between Sparkplug and TurboFan.

It provides better performance for medium-running code without waiting for the most aggressive optimization stage.

Think of it as a "fast optimizer."

---

# Step 6 — TurboFan

TurboFan is V8's most advanced optimizing compiler.

When V8 detects that a function is executed frequently, TurboFan generates highly optimized machine code.

This optimized code can execute significantly faster than the initial interpreted version.

This process is one of the key ideas behind **Just-In-Time (JIT) Compilation**.

We'll explore JIT in detail later.

---

# Why Doesn't V8 Optimize Everything Immediately?

Imagine compiling an entire 500-page book before reading the first page.

It would take a long time before you could start reading.

Instead, V8 follows a smarter strategy.

1. Execute quickly.
2. Observe which code is used most often.
3. Optimize only the important parts.

This balance gives JavaScript both:

- Fast startup
- Excellent long-term performance

---

# V8 Execution Pipeline

The complete journey looks like this:

```text
Developer

      │

      ▼

JavaScript Source Code

      │

      ▼

Parser

      │

      ▼

Abstract Syntax Tree

      │

      ▼

Ignition

      │

      ▼

Bytecode

      │

      ▼

Sparkplug

      │

      ▼

Maglev

      │

      ▼

TurboFan

      │

      ▼

Optimized Machine Code

      │

      ▼

CPU Executes Instructions
```

This pipeline is a simplified model, but it captures the major execution stages.

---

# Why Is This Important for Angular Developers?

Angular applications contain thousands of JavaScript functions.

Examples include:

- Component methods
- Lifecycle hooks
- Event handlers
- RxJS operators
- Change detection logic

When these functions execute repeatedly, V8 can optimize them.

Writing predictable, consistent code gives the engine more opportunities to optimize execution.

This is one reason performance best practices matter in Angular.

---

# Interview Perspective

### Question

**What is V8?**

A strong answer:

> V8 is Google's open-source JavaScript Engine. It parses JavaScript, creates an Abstract Syntax Tree, generates bytecode using Ignition, and progressively optimizes frequently executed code using compilers such as Sparkplug, Maglev, and TurboFan before producing optimized machine code.

---

### Question

**Why doesn't V8 generate optimized machine code immediately?**

Answer:

Because optimization has a cost. V8 first executes code quickly and only spends time optimizing functions that are executed frequently.

---

# Common Mistakes

❌ Thinking V8 only interprets JavaScript.

❌ Assuming V8 immediately compiles every function into highly optimized machine code.

❌ Believing the Parser executes JavaScript.

❌ Confusing bytecode with machine code.

❌ Thinking optimization happens only once.

---

# Key Takeaways

- V8 is Google's JavaScript Engine.
- It uses multiple execution stages instead of a single interpreter.
- The Parser validates code and builds an AST.
- Ignition generates bytecode for fast startup.
- Sparkplug and Maglev improve execution speed.
- TurboFan generates highly optimized machine code.
- This multi-stage approach balances startup performance with runtime efficiency.

---

## Next Section

In **Section 7 — Parsing & Tokenization**, we'll zoom into the **Parser** and study how JavaScript source code is broken into tokens, validated, and transformed into an **Abstract Syntax Tree (AST)** before execution begins.

---

---

# Section 7 — Parsing & Tokenization

> *"Before a JavaScript Engine can execute your code, it must first understand what you have written."*

---

## Learning Objectives

After completing this section, you will be able to:

- Understand what parsing is.
- Explain what tokenization means.
- Understand lexical analysis.
- Differentiate source code from tokens.
- Explain why parsing happens before execution.
- Understand why syntax errors occur before a program runs.
- Connect parsing with the next stage: the Abstract Syntax Tree (AST).

---

# Introduction

Imagine someone gives you a book written in a language you've never seen before.

Before understanding the meaning of the sentences, you must first:

- Identify individual words.
- Recognize punctuation.
- Understand sentence structure.
- Verify that the grammar is correct.

A JavaScript Engine behaves in a very similar way.

When you write JavaScript, the engine does **not** immediately execute it.

Instead, it first tries to understand the program.

This understanding process begins with **Parsing**.

---

# What is Parsing?

Parsing is the process of reading JavaScript source code and verifying that it follows the rules of the JavaScript language.

For example:

```javascript
const username = "Manish";

console.log(username);
```

To us, this looks like two simple lines.

To the JavaScript Engine, it is merely a sequence of characters.

The engine must determine:

- Is this valid JavaScript?
- Are all keywords used correctly?
- Are brackets balanced?
- Are strings properly closed?
- Are operators in valid positions?

Only after answering these questions can execution continue.

---

# Why Can't the Engine Execute Source Code Directly?

Consider this code:

```javascript
const age = 25;
```

To us, it clearly means:

> Create a constant variable called `age` and assign it the value `25`.

But to a computer, the source code initially looks like nothing more than characters:

```text
c
o
n
s
t

a
g
e

=

2
5
;
```

The engine must organize these characters into meaningful units.

This process is called **Tokenization**.

---

# What is Tokenization?

Tokenization is the process of breaking source code into small meaningful pieces called **tokens**.

Think of tokens as the vocabulary of a programming language.

For the following code:

```javascript
const age = 25;
```

The engine generates tokens similar to:

```text
KEYWORD      -> const

IDENTIFIER   -> age

OPERATOR     -> =

NUMBER        -> 25

SEMICOLON    -> ;
```

Instead of reading one character at a time, the parser now understands the program as a collection of meaningful language elements.

---

# Visualizing Tokenization

Source Code:

```javascript
const age = 25;
```

↓

Characters

```text
c o n s t a g e = 2 5 ;
```

↓

Tokens

```text
KEYWORD

IDENTIFIER

ASSIGNMENT OPERATOR

NUMERIC LITERAL

SEMICOLON
```

↓

Parser continues with the next stage.

---

# Common Types of Tokens

JavaScript contains many different token types.

| Token Type | Example |
|------------|---------|
| Keyword | `const`, `let`, `if`, `return` |
| Identifier | `user`, `age`, `calculateTotal` |
| Operator | `+`, `-`, `*`, `/`, `=` |
| Literal | `"Hello"`, `25`, `true` |
| Separator | `(`, `)`, `{`, `}`, `[`, `]` |
| Punctuation | `;`, `,`, `.` |

These tokens become the building blocks of every JavaScript program.

---

# Lexical Analysis

Tokenization is part of a broader process called **Lexical Analysis**.

During lexical analysis, the engine scans the source code from left to right.

Its responsibilities include:

- Reading characters.
- Grouping characters into tokens.
- Identifying keywords.
- Identifying identifiers.
- Recognizing operators.
- Ignoring unnecessary whitespace.
- Ignoring comments.

For example:

```javascript
// User information

const age = 25;
```

The comment is ignored during execution, while the remaining code is converted into tokens.

---

# Why Parsing Happens Before Execution

Consider this invalid program:

```javascript
const user = ;
```

What should the engine execute?

There is no value after the assignment operator.

Instead of executing partial code, the parser immediately reports:

```text
SyntaxError: Unexpected token ';'
```

Execution never starts.

This is why syntax errors are called **parse-time errors**.

The program fails before any JavaScript is executed.

---

# Another Example

Valid code:

```javascript
function greet() {
    console.log("Hello");
}
```

Invalid code:

```javascript
function greet( {
    console.log("Hello");
}
```

The parser detects the missing parenthesis and stops the program immediately.

---

# Parsing Is Not Execution

This distinction is extremely important.

Many beginners believe parsing and execution happen together.

They do not.

The engine first checks:

- Is the code valid?
- Can it understand the program?

Only after successful parsing does execution begin.

Think of it like compiling an examination paper before grading it.

If the paper is unreadable, grading cannot begin.

---

# Real-World Example

Consider this Angular component:

```typescript
@Component({
  selector: 'app-user'
})
export class UserComponent {

    name = "Manish";

    greet() {
        console.log(this.name);
    }

}
```

Before this reaches the browser:

1. TypeScript is transpiled into JavaScript.
2. Angular bundles the application.
3. The browser downloads the bundle.
4. V8 begins parsing the JavaScript.
5. Tokens are generated.
6. The parser validates the syntax.
7. Only then can execution continue.

Even a tiny syntax error in the generated JavaScript would stop execution before Angular starts.

---

# Angular Connection

Although Angular developers primarily write TypeScript, the browser never executes TypeScript directly.

The workflow is:

```text
TypeScript

      │

      ▼

Angular Compiler

      │

      ▼

JavaScript

      │

      ▼

Parser

      │

      ▼

Tokens

      │

      ▼

Abstract Syntax Tree

      │

      ▼

Execution
```

Everything eventually passes through the JavaScript parser.

---

# Interview Perspective

### Question

**What is parsing?**

A strong answer:

> Parsing is the process by which the JavaScript Engine analyzes source code, validates its syntax, and prepares an internal representation that can later be executed.

---

### Question

**What is tokenization?**

A strong answer:

> Tokenization is the process of breaking JavaScript source code into small meaningful units called tokens, such as keywords, identifiers, operators, literals, and punctuation.

---

### Question

**Does JavaScript execute before parsing?**

Answer:

No.

Parsing always occurs before execution.

If parsing fails, execution never begins.

---

# Common Mistakes

❌ Thinking parsing means execution.

❌ Assuming tokenization is optional.

❌ Believing syntax errors occur during execution.

❌ Confusing characters with tokens.

❌ Assuming comments become part of the executable program.

---

# Key Takeaways

- Parsing is the first major stage after the engine receives source code.
- The parser validates JavaScript syntax.
- Tokenization converts source code into meaningful language tokens.
- Lexical analysis identifies keywords, identifiers, operators, literals, and punctuation.
- Syntax errors are detected before execution begins.
- Parsing prepares the program for the creation of the Abstract Syntax Tree (AST).

---

## Next Section

In **Section 8 — Abstract Syntax Tree (AST)**, we'll see how the parser transforms tokens into a tree-like structure that represents the entire program.

The AST is one of the most important internal data structures in every modern JavaScript Engine and forms the foundation for interpretation, compilation, optimization, and code execution.

---

---

# Section 8 — Abstract Syntax Tree (AST)

> *"Once the JavaScript Engine understands your code through tokens, it still cannot execute it directly. First, it builds a structured representation of your program called the Abstract Syntax Tree (AST)."*

---

## Learning Objectives

After completing this section, you will be able to:

- Understand what an Abstract Syntax Tree (AST) is.
- Explain why JavaScript Engines build an AST.
- Understand how tokens are transformed into a tree.
- Read simple AST structures.
- Explain how the AST is used by the JavaScript Engine.
- Understand why tools like Angular, TypeScript, Babel and ESLint rely heavily on ASTs.

---

# Introduction

In the previous section, we learned that the Parser converts source code into **Tokens**.

However, tokens alone are not enough.

Consider the following code:

```javascript
const total = price * quantity;
```

The parser knows:

```text
KEYWORD

IDENTIFIER

OPERATOR

IDENTIFIER

OPERATOR

IDENTIFIER
```

But it still doesn't understand questions like:

- Which variable is being declared?
- Which operator executes first?
- Which value belongs to which variable?
- Is multiplication happening before assignment?
- Which expression should be evaluated first?

To answer these questions, the parser builds a much richer data structure called the **Abstract Syntax Tree (AST).**

---

# What is an Abstract Syntax Tree?

An **Abstract Syntax Tree (AST)** is a tree-like representation of your JavaScript program.

Instead of storing code as plain text, the engine stores it as interconnected nodes.

Each node represents one meaningful part of the program.

Think of it like a family tree.

Instead of parents and children, the AST contains:

- Variables
- Functions
- Expressions
- Operators
- Loops
- Objects
- Classes
- Statements

This structure makes the program much easier for the engine to understand.

---

# Why is it Called "Abstract"?

Let's break the name into three parts.

### Abstract

The tree ignores unnecessary details like:

- Spaces
- Tabs
- Line breaks
- Comments

The following code:

```javascript
const age=25;
```

and

```javascript
const    age     =      25;
```

produce almost the same AST.

Whitespace has no meaning here.

---

### Syntax

The AST represents the grammatical structure of JavaScript.

It understands things like:

- Variables
- Functions
- Expressions
- Loops
- Objects
- Classes

---

### Tree

The program is represented as connected parent-child nodes.

Everything becomes hierarchical.

---

# Example 1

Consider:

```javascript
const age = 25;
```

Conceptually, the AST looks like:

```text
VariableDeclaration
│
├── Kind
│      └── const
│
└── VariableDeclarator
       │
       ├── Identifier
       │      └── age
       │
       └── NumericLiteral
              └── 25
```

Notice that this is much richer than a simple list of tokens.

The engine now understands that:

- a variable is being declared,
- its name is `age`,
- its value is `25`,
- and it is declared using `const`.

---

# Example 2

Now consider:

```javascript
const total = price + tax;
```

The AST becomes:

```text
VariableDeclaration
│
└── VariableDeclarator
      │
      ├── Identifier(total)
      │
      └── BinaryExpression(+)
             │
             ├── Identifier(price)
             │
             └── Identifier(tax)
```

The parser now understands:

```
price + tax
```

is one expression.

---

# Example 3

Consider:

```javascript
const result = a + b * c;
```

Most beginners read it left to right.

The parser does not.

It understands operator precedence.

AST:

```text
Assignment

│

└── +

     ├── a

     └── *

          ├── b

          └── c
```

Notice something interesting.

Multiplication appears lower in the tree.

That tells the engine:

```
b * c
```

must execute before:

```
a + ...
```

The AST naturally preserves JavaScript operator precedence.

---

# How is the AST Created?

The overall process looks like this:

```text
JavaScript Source Code

        │

        ▼

Lexical Analysis

        │

        ▼

Tokens

        │

        ▼

Parser

        │

        ▼

Abstract Syntax Tree (AST)
```

The parser reads the tokens one by one.

Using JavaScript grammar rules, it gradually constructs the tree.

---

# Why Doesn't the Engine Execute Tokens Directly?

Imagine reading this list:

```text
IDENTIFIER

NUMBER

PLUS

IDENTIFIER

EQUALS

RETURN
```

It is impossible to understand the actual program.

Now compare that with a tree.

```text
Function

│

└── Return

      │

      └── BinaryExpression
```

The tree immediately reveals the program's structure.

This makes analysis, optimization and execution much easier.

---

# How V8 Uses the AST

After building the AST, V8 performs many tasks.

It can:

- Validate program structure.
- Detect syntax problems.
- Generate bytecode.
- Optimize expressions.
- Perform static analysis.
- Apply compiler optimizations.
- Generate machine code later.

The AST is the foundation for almost every later stage inside the engine.

---

# AST Beyond the JavaScript Engine

The AST is not used only by V8.

Many popular development tools depend on it.

| Tool | Why it Uses AST |
|-------|-----------------|
| TypeScript | Type checking and transpilation |
| Angular Compiler | Template and metadata analysis |
| Babel | Transform modern JavaScript into older versions |
| ESLint | Detect code issues |
| Prettier | Automatically format code |
| SWC | Fast compilation |
| esbuild | Bundling and transformations |

This means the AST is one of the most important concepts in the JavaScript ecosystem.

---

# Angular Connection

Angular also performs AST-based analysis.

For example:

```html
<button (click)="save()">
```

Angular parses templates into its own internal syntax tree.

Similarly,

TypeScript is parsed into an AST before being transpiled into JavaScript.

Finally,

the generated JavaScript is parsed again by the browser's JavaScript Engine.

Simplified flow:

```text
Angular Template

        │

        ▼

Angular Template AST

        │

        ▼

TypeScript

        │

        ▼

TypeScript AST

        │

        ▼

JavaScript

        │

        ▼

JavaScript AST

        │

        ▼

V8 Execution
```

Multiple ASTs are created throughout the build and execution pipeline.

---

# Real-World Example

Suppose you rename a variable in VS Code.

```javascript
userName
```

↓

```javascript
customerName
```

How does the editor know which occurrences to rename?

It doesn't search for plain text.

It uses the AST to understand which identifier belongs to which variable.

This prevents incorrect replacements.

---

# Interview Perspective

### Question

**What is an Abstract Syntax Tree (AST)?**

A strong answer:

> An Abstract Syntax Tree is a hierarchical representation of JavaScript source code created by the parser. It represents the grammatical structure of a program and is used by the JavaScript Engine for analysis, bytecode generation, optimization, and execution.

---

### Question

**Why is an AST required?**

Answer:

Because tokens alone do not describe relationships between language constructs.

The AST provides the structure needed for analysis, optimization, and execution.

---

### Question

**Do only JavaScript Engines use ASTs?**

Answer:

No.

Many tools—including TypeScript, Angular Compiler, Babel, ESLint, Prettier, and esbuild—use ASTs to analyze and transform code.

---

# Common Mistakes

❌ Thinking the AST is the same as tokens.

❌ Assuming the AST contains comments and formatting.

❌ Believing only browsers use ASTs.

❌ Confusing parsing with AST creation.

❌ Assuming the AST is machine code.

---

# Key Takeaways

- The AST is a structured representation of JavaScript code.
- It is created by the parser after tokenization.
- The AST preserves the grammatical relationships within the program.
- Modern JavaScript Engines use the AST for execution and optimization.
- Many developer tools also rely on ASTs to understand and transform code.

---

## Next Section

In **Section 9 — Interpreter vs Compiler vs Just-In-Time (JIT) Compilation**, we'll answer one of the most debated JavaScript interview questions:

> **"Is JavaScript an interpreted language, a compiled language, or both?"**

We'll also explore how modern engines like V8 combine interpretation and compilation to achieve both fast startup and high runtime performance.

---

---

# Section 9 — Interpreter vs Compiler vs Just-In-Time (JIT) Compilation

> *"One of the most common JavaScript interview questions is: 'Is JavaScript an interpreted language or a compiled language?' The real answer is more interesting than either option."*

---

## Learning Objectives

After completing this section, you will be able to:

- Understand the difference between an Interpreter and a Compiler.
- Explain the advantages and disadvantages of both approaches.
- Understand why modern JavaScript Engines use both interpretation and compilation.
- Explain what Just-In-Time (JIT) Compilation is.
- Understand how V8 executes JavaScript efficiently.
- Answer advanced interview questions about JavaScript execution.

---

# Introduction

If you've attended JavaScript interviews or watched programming tutorials, you've probably heard statements like:

> "JavaScript is an interpreted language."

Others say:

> "JavaScript is compiled."

Both statements are incomplete.

Modern JavaScript Engines, such as **V8**, **SpiderMonkey**, and **JavaScriptCore**, use a combination of **interpretation** and **compilation**.

Understanding this execution model is one of the biggest differences between someone who simply writes JavaScript and someone who understands how JavaScript actually works.

---

# What is an Interpreter?

An **Interpreter** reads your source code and executes it immediately without first generating a complete machine-code executable.

Imagine reading a book sentence by sentence.

You read one sentence.

Understand it.

Act on it.

Then move to the next sentence.

That's exactly how an interpreter works.

Example:

```javascript
console.log("Hello");

console.log("Angular");
```

An interpreter reads the code one instruction at a time and starts execution immediately.

---

## Advantages of an Interpreter

- Faster startup.
- No separate build step.
- Easier debugging.
- Ideal for interactive applications.

---

## Disadvantages

- Repeated execution of the same code can be slower.
- Less opportunity for aggressive optimization.
- Performance may decrease for CPU-intensive programs.

---

# What is a Compiler?

A **Compiler** translates the entire source program into machine code before execution begins.

Think of translating an entire book before anyone starts reading it.

Workflow:

```text
Source Code

      │

      ▼

Compiler

      │

      ▼

Machine Code

      │

      ▼

Program Executes
```

Languages such as C and C++ traditionally follow this model.

---

## Advantages of a Compiler

- Very fast execution.
- Extensive optimization opportunities.
- Machine code is ready before execution starts.

---

## Disadvantages

- Compilation takes time.
- Startup is slower.
- Every code change requires recompilation.

---

# Interpreter vs Compiler

| Feature | Interpreter | Compiler |
|---------|-------------|----------|
| Execution | Line-by-line | Entire program |
| Startup Speed | Fast | Slower |
| Runtime Performance | Moderate | Fast |
| Optimization | Limited | Extensive |
| Debugging | Easier | Slightly harder |
| Example | Traditional scripting languages | C, C++ (classic workflow) |

Modern JavaScript Engines combine the strengths of both approaches.

---

# Why Not Use Only an Interpreter?

Imagine a function that executes one million times.

```javascript
function square(x) {
    return x * x;
}

for (let i = 0; i < 1_000_000; i++) {
    square(i);
}
```

If the engine interprets the function every time, it repeatedly performs the same work.

This wastes CPU cycles.

---

# Why Not Compile Everything Immediately?

Now imagine a huge application containing 20,000 functions.

Perhaps only 100 of those functions are executed frequently.

Compiling all 20,000 functions into highly optimized machine code would:

- Increase startup time.
- Consume unnecessary CPU resources.
- Waste memory on code that may never run.

Clearly, there needs to be a smarter strategy.

---

# The Solution — Just-In-Time (JIT) Compilation

Modern JavaScript Engines solve this problem using **Just-In-Time (JIT) Compilation**.

Instead of choosing between interpretation and compilation, they combine both.

The strategy is simple:

1. Start execution quickly.
2. Observe how the program behaves.
3. Detect frequently executed ("hot") code.
4. Optimize only that code.
5. Continue running optimized machine code.

This approach delivers:

- Fast startup.
- High runtime performance.
- Efficient memory usage.

---

# High-Level JIT Workflow

```text
JavaScript Source Code

          │

          ▼

Parser

          │

          ▼

Abstract Syntax Tree

          │

          ▼

Ignition Interpreter

          │

          ▼

Bytecode Execution

          │

          ▼

Runtime Profiling

          │

          ▼

Frequently Executed?

      Yes ─────────────► TurboFan

                          │

                          ▼

                Optimized Machine Code

                          │

                          ▼

                       CPU
```

Notice that not every function reaches the final optimization stage.

Only code that benefits from optimization is compiled aggressively.

---

# What is "Hot Code"?

Hot code refers to code that executes repeatedly.

Example:

```javascript
function calculateTotal(price, quantity) {
    return price * quantity;
}

for (let i = 0; i < 500000; i++) {
    calculateTotal(i, 2);
}
```

Because `calculateTotal()` runs hundreds of thousands of times, the engine identifies it as a candidate for optimization.

The optimized version executes much faster than repeatedly interpreting the function.

---

# What About Functions That Execute Only Once?

Consider:

```javascript
function showWelcomeMessage() {
    console.log("Welcome!");
}

showWelcomeMessage();
```

This function executes only once.

Compiling it aggressively would cost more than the performance benefit gained.

Therefore, V8 usually keeps such code in the faster startup path instead of spending time heavily optimizing it.

---

# Why JIT Matters

Without JIT:

- JavaScript applications would start quickly but remain slower over time.

Without interpretation:

- JavaScript applications would spend too much time compiling before they could even start.

JIT combines the advantages of both approaches.

This is one of the key reasons modern JavaScript applications can scale from simple scripts to complex enterprise applications.

---

# Real-World Example

Imagine opening a large Angular application.

During startup:

- Thousands of functions are loaded.
- Only a fraction are executed immediately.
- Many routes are never visited.
- Some features are rarely used.

V8 avoids wasting time optimizing every function.

Instead, it watches how users interact with the application and optimizes the code paths that are actually exercised.

---

# Angular Connection

Angular applications contain many kinds of functions:

- Component methods
- Lifecycle hooks
- Event handlers
- RxJS operators
- Pipe transformations
- Utility functions

Frequently executed code—such as methods involved in repeated rendering or intensive calculations—can benefit from V8's optimization pipeline.

This is one reason performance profiling should focus on hot paths rather than optimizing rarely executed code.

---

# Interview Perspective

### Question

**Is JavaScript an interpreted language?**

A beginner might answer:

> Yes.

A stronger answer is:

> Historically, JavaScript was often described as an interpreted language. Modern JavaScript Engines such as V8 use a combination of interpretation and Just-In-Time (JIT) compilation. They begin execution quickly using an interpreter and progressively compile frequently executed code into optimized machine code.

---

### Question

**What is JIT Compilation?**

Answer:

> Just-In-Time Compilation is a runtime optimization technique in which the JavaScript Engine first executes code quickly, monitors execution, identifies frequently executed functions, and compiles those functions into optimized machine code to improve performance.

---

### Question

**Why doesn't V8 compile every function immediately?**

Answer:

Because compiling everything would increase startup time and waste resources on code that may never execute. V8 optimizes only the code that provides a meaningful performance benefit.

---

# Common Mistakes

❌ Saying JavaScript is "only interpreted."

❌ Saying JavaScript is "only compiled."

❌ Thinking every function is immediately optimized.

❌ Assuming JIT happens before execution begins.

❌ Confusing bytecode with machine code.

---

# Key Takeaways

- An Interpreter executes code quickly with minimal upfront work.
- A Compiler generates machine code before execution.
- Modern JavaScript Engines combine both approaches.
- JIT Compilation optimizes frequently executed code during runtime.
- V8 balances fast startup with excellent long-term performance.
- This hybrid execution model is a major reason JavaScript performs well in modern applications.

---

## Next Section

In **Section 10 — JavaScript Execution Pipeline**, we'll connect everything you've learned so far into one complete flow.

We'll trace a JavaScript program from the moment you save a `.js` file all the way to machine instructions executed by the CPU, tying together parsing, tokenization, AST creation, interpretation, JIT compilation, optimization, and execution into a single end-to-end pipeline.

---

---

# Section 10 — JavaScript Execution Pipeline

> *"So far, we've learned about the JavaScript Engine, Parsing, Tokenization, AST, and JIT Compilation separately. In this section, we'll connect everything together and follow the complete lifecycle of a JavaScript program from source code to CPU execution."*

---

## Learning Objectives

After completing this section, you will be able to:

- Explain the complete lifecycle of JavaScript code.
- Understand how each stage connects with the next.
- Describe how V8 transforms source code into machine instructions.
- Understand where optimization occurs.
- Explain the complete execution pipeline during interviews.
- Relate this pipeline to Angular applications.

---

# Introduction

Imagine you've just written the following JavaScript program.

```javascript
function greet(name) {
    return `Hello ${name}`;
}

console.log(greet("Manish"));
```

You save the file.

You refresh your browser.

Within milliseconds, the output appears:

```text
Hello Manish
```

It looks simple.

However, before that output appears, your code passes through a sophisticated pipeline involving multiple stages inside the JavaScript Engine.

Understanding this journey is one of the most valuable skills for any JavaScript or Angular developer.

---

# The Complete Journey

At a high level, the execution pipeline looks like this:

```text
Developer
    │
    ▼
JavaScript Source Code
    │
    ▼
Lexical Analysis
    │
    ▼
Tokenization
    │
    ▼
Parser
    │
    ▼
Abstract Syntax Tree (AST)
    │
    ▼
Ignition Interpreter
    │
    ▼
Bytecode
    │
    ▼
Runtime Execution
    │
    ▼
Profiler
    │
    ▼
Hot Code?
    │
 ┌──┴──┐
 │     │
No    Yes
 │     │
 ▼     ▼
Continue  TurboFan / Maglev Optimization
           │
           ▼
 Optimized Machine Code
           │
           ▼
          CPU
           │
           ▼
      Program Output
```

This pipeline summarizes everything you've learned in this chapter.

Now let's study each stage.

---

# Stage 1 — Writing Source Code

Everything begins with human-readable JavaScript.

```javascript
const price = 100;
const tax = 18;

console.log(price + tax);
```

At this point, your code is simply text inside a file.

The CPU cannot understand it.

---

# Stage 2 — Lexical Analysis

The engine starts scanning your source code character by character.

Its responsibilities include:

- Reading characters
- Identifying keywords
- Identifying identifiers
- Ignoring whitespace
- Ignoring comments
- Preparing for tokenization

Example:

```javascript
const price = 100;
```

Characters become meaningful language elements.

---

# Stage 3 — Tokenization

The source code is divided into tokens.

Example:

```javascript
const price = 100;
```

becomes conceptually:

```text
KEYWORD

IDENTIFIER

ASSIGNMENT OPERATOR

NUMERIC LITERAL

SEMICOLON
```

Tokens provide meaning, but not relationships.

The parser still needs to understand how these tokens fit together.

---

# Stage 4 — Parsing

The parser validates the program.

It answers questions such as:

- Is the syntax valid?
- Are brackets balanced?
- Are keywords correctly placed?
- Are expressions legal?

If the parser detects an error:

```javascript
const total = ;
```

execution stops immediately with a `SyntaxError`.

No JavaScript code runs.

---

# Stage 5 — Building the AST

After successful parsing, the engine creates the **Abstract Syntax Tree (AST).**

Instead of plain text, the program is now represented as interconnected nodes.

Example:

```javascript
const total = price + tax;
```

Conceptually becomes:

```text
VariableDeclaration

      │

      ├── Identifier(total)

      │

      └── BinaryExpression(+)

             ├── Identifier(price)

             └── Identifier(tax)
```

The AST captures the structure of the program.

---

# Stage 6 — Ignition Generates Bytecode

V8 now passes the AST to **Ignition**.

Ignition converts the AST into **bytecode**.

Bytecode is a lower-level representation that is much faster to execute than raw source code.

It is still **not** machine code.

Think of bytecode as an intermediate language understood by the engine.

---

# Stage 7 — Executing Bytecode

The engine begins executing the generated bytecode.

During execution:

- Variables receive values.
- Functions are called.
- Expressions are evaluated.
- Objects are created.
- Memory is allocated.

At this stage, your application actually begins running.

---

# Stage 8 — Runtime Profiling

While the application is running, V8 continuously observes execution.

It collects information such as:

- Which functions execute frequently?
- Which loops consume the most time?
- Which object shapes remain stable?
- Which functions become "hot"?

This information guides later optimizations.

---

# Stage 9 — Optimization

If V8 determines that a function executes frequently, it sends it to the optimizing compiler.

For example:

```javascript
function multiply(a, b) {
    return a * b;
}

for (let i = 0; i < 1_000_000; i++) {
    multiply(i, 2);
}
```

Since `multiply()` is called repeatedly, V8 may replace its initial execution path with optimized machine code.

This significantly improves performance.

---

# Stage 10 — Machine Code Execution

Finally, the optimized instructions reach the CPU.

The CPU executes machine instructions directly.

This is the fastest execution stage.

The result is then returned to the application.

---

# Putting Everything Together

The complete execution lifecycle can be summarized as:

```text
Write JavaScript
        │
        ▼
Lexical Analysis
        │
        ▼
Tokenization
        │
        ▼
Parsing
        │
        ▼
Abstract Syntax Tree
        │
        ▼
Ignition
        │
        ▼
Bytecode
        │
        ▼
Execution
        │
        ▼
Profiler
        │
        ▼
Optimization
        │
        ▼
Machine Code
        │
        ▼
CPU
        │
        ▼
Output
```

This is the mental model you should remember.

---

# What Happens if Something Goes Wrong?

Different stages detect different kinds of problems.

| Stage | Possible Error |
|--------|----------------|
| Parsing | SyntaxError |
| Execution | ReferenceError |
| Execution | TypeError |
| Execution | RangeError |
| Runtime | Memory Issues |
| Optimization | Deoptimization (engine falls back to a less optimized version when assumptions are no longer valid) |

Understanding **where** an error occurs makes debugging much easier.

---

# Real-World Example

Imagine you build your Angular application.

```bash
ng build
```

The process is roughly:

```text
TypeScript

      │

      ▼

Angular Compiler

      │

      ▼

JavaScript Bundle

      │

      ▼

Browser Downloads Bundle

      │

      ▼

V8 Pipeline

      │

      ▼

Lexical Analysis

      │

      ▼

Parser

      │

      ▼

AST

      │

      ▼

Bytecode

      │

      ▼

Execution

      │

      ▼

Angular Bootstraps

      │

      ▼

Application Starts
```

Every Angular application ultimately passes through this execution pipeline.

---

# Why Understanding the Pipeline Matters

When you understand the pipeline, many JavaScript concepts become easier:

- Why syntax errors occur before execution.
- Why runtime errors happen after execution begins.
- Why V8 optimizes some functions but not others.
- Why performance profiling focuses on "hot" code.
- Why stable code patterns often perform better than unpredictable ones.

This knowledge also helps you reason about application performance instead of relying on guesswork.

---

# Interview Perspective

### Question

**Explain the JavaScript execution pipeline.**

A strong answer:

> JavaScript source code first undergoes lexical analysis and tokenization. The parser validates the syntax and builds an Abstract Syntax Tree (AST). V8's Ignition interpreter converts the AST into bytecode, which begins execution. During runtime, the engine profiles execution, identifies frequently executed code, and passes hot code to optimizing compilers such as Maglev and TurboFan. These compilers generate optimized machine code, which is then executed by the CPU.

---

### Question

**Which stage creates the AST?**

Answer:

The **Parser** creates the AST after successful tokenization and syntax validation.

---

### Question

**Does bytecode execute directly on the CPU?**

Answer:

No.

The CPU executes **machine code**. Bytecode is an intermediate representation used by the JavaScript Engine.

---

# Common Mistakes

❌ Thinking parsing and execution happen simultaneously.

❌ Assuming the parser generates machine code.

❌ Believing bytecode is the same as machine code.

❌ Thinking every function is optimized immediately.

❌ Ignoring the runtime profiling stage.

---

# Key Takeaways

- JavaScript execution consists of multiple stages.
- Source code is first analyzed before execution.
- Parsing creates the Abstract Syntax Tree.
- Ignition converts the AST into bytecode.
- Runtime profiling identifies hot code.
- Maglev and TurboFan optimize frequently executed code.
- The CPU ultimately executes optimized machine code.

---

## Next Section

In **Section 11 — Memory Management & Garbage Collection (Introduction)**, we'll explore how the JavaScript Engine allocates memory, stores variables and objects, manages the Stack and Heap, and automatically reclaims unused memory through Garbage Collection.

---

---

# Section 11 — Memory Management & Garbage Collection (Introduction)

> *"Every variable you declare and every object you create occupies memory. Understanding how the JavaScript Engine manages that memory is essential for writing efficient applications and avoiding memory leaks."*

---

## Learning Objectives

After completing this section, you will be able to:

- Understand why memory management is important.
- Learn how JavaScript allocates memory.
- Understand the difference between Stack Memory and Heap Memory.
- Learn what Garbage Collection is.
- Understand why memory leaks happen.
- Relate memory management concepts to Angular applications.

---

# Introduction

Whenever you write JavaScript code, memory is required.

Consider the following example:

```javascript
const username = "Manish";

const user = {
    id: 1,
    city: "Raipur"
};

function greet() {
    console.log(username);
}
```

Where are these values stored?

Who allocates memory?

Who removes the memory after it is no longer needed?

Unlike languages such as C or C++, JavaScript developers do not manually allocate or free memory.

Instead, the **JavaScript Engine automatically manages memory** for us.

This automatic management is one of JavaScript's greatest strengths.

---

# Why Does JavaScript Need Memory?

Memory is required to store:

- Variables
- Functions
- Objects
- Arrays
- Strings
- Numbers
- Classes
- Closures
- Execution Contexts

Without memory, JavaScript programs would have nowhere to store data while executing.

---

# Memory Lifecycle

Every value in JavaScript follows a simple lifecycle.

```text
Create Value
      │
      ▼
Allocate Memory
      │
      ▼
Use the Value
      │
      ▼
Value Becomes Unreachable
      │
      ▼
Garbage Collector Frees Memory
```

This entire process is handled automatically by the JavaScript Engine.

---

# Memory Allocation

Whenever JavaScript creates a value, the engine allocates memory.

Example:

```javascript
let age = 25;
```

Memory is allocated for:

- Variable name → `age`
- Value → `25`

Similarly:

```javascript
const user = {
    name: "Manish"
};
```

Memory is allocated for:

- Variable reference
- Object
- Object properties
- String values

---

# Two Main Memory Areas

The JavaScript Engine primarily uses two memory regions:

```text
Memory

├── Stack
│
└── Heap
```

Each serves a different purpose.

---

# Stack Memory

The **Stack** is used for small, short-lived data.

Typically, it stores:

- Primitive values (implementation detail varies by engine)
- Function call information
- Execution Contexts
- References to heap objects

Think of the stack as a stack of plates.

```text
Top

┌──────────────┐
│ Function C   │
├──────────────┤
│ Function B   │
├──────────────┤
│ Function A   │
└──────────────┘

Bottom
```

The last function added is the first one removed.

This behavior is called **LIFO (Last In, First Out).**

---

# Heap Memory

The **Heap** stores larger and dynamically allocated data.

Examples include:

- Objects
- Arrays
- Functions
- Maps
- Sets
- Large strings

Example:

```javascript
const user = {
    name: "Manish",
    age: 27
};
```

The object itself is stored in the Heap.

The variable `user` refers to that object.

---

# Stack vs Heap

| Stack | Heap |
|--------|------|
| Faster access | Slightly slower |
| Stores execution information | Stores objects and dynamic data |
| Automatically grows and shrinks with function calls | Managed by the Garbage Collector |
| Organized | More flexible |

> **Note:** This is a simplified mental model. Modern JavaScript engines optimize memory in sophisticated ways, and the exact storage strategy is an implementation detail.

---

# Example

```javascript
let age = 25;

let person = {
    name: "Manish"
};
```

Conceptually:

```text
Stack

age ─────────────► 25

person ──────────┐
                 │
                 ▼

Heap

Object
│
├── name
└── "Manish"
```

The variable stores a reference to the object, while the object itself resides in heap memory.

---

# What is Garbage Collection?

Imagine a classroom.

Students write notes on the board.

Eventually the notes are no longer needed.

Someone has to erase them.

Otherwise, the board becomes full.

Garbage Collection works in a similar way.

When an object is no longer reachable by the program, the JavaScript Engine can reclaim its memory.

This prevents memory from growing indefinitely.

---

# Example

```javascript
function demo() {

    const message = "Temporary";

}

demo();
```

After `demo()` finishes executing, `message` is no longer accessible.

Since nothing can reference it anymore, its memory becomes eligible for Garbage Collection.

---

# Reachability

Modern JavaScript Engines determine whether memory can be reclaimed by checking **reachability**.

If an object can still be reached from the running program, it must remain in memory.

If it becomes unreachable, it can eventually be removed.

Example:

```javascript
let user = {
    name: "Manish"
};

user = null;
```

After assigning `null`, the original object is no longer referenced.

Eventually, the Garbage Collector may reclaim its memory.

---

# Memory Leaks

Automatic Garbage Collection does **not** mean memory leaks are impossible.

A memory leak occurs when objects remain reachable even though they are no longer useful.

Common causes include:

- Forgotten event listeners
- Global variables
- Long-lived timers
- Closures retaining unnecessary data
- Cached objects that are never cleared

We'll study memory leaks in detail later.

---

# Angular Connection

Memory management is especially important in Angular applications.

Examples of common memory leaks include:

```typescript
this.subscription = this.userService.users$.subscribe();
```

If the subscription is never cleaned up (where appropriate), it can keep objects alive longer than intended.

Other examples include:

- Event listeners that are not removed
- Intervals that continue running
- Detached DOM references
- Services holding unnecessary data

Understanding how the JavaScript Engine manages memory makes these issues easier to diagnose.

---

# Real-World Example

Imagine an e-commerce application.

Every product loaded from the server creates JavaScript objects.

```javascript
products.push(product);
```

If products are continuously added but never removed when no longer needed, memory usage grows.

Eventually:

- Performance decreases.
- Garbage Collection becomes more frequent.
- The application may feel sluggish.

Good application design helps avoid unnecessary memory retention.

---

# Interview Perspective

### Question

**Who allocates memory in JavaScript?**

Answer:

The JavaScript Engine automatically allocates memory whenever values, objects, functions, or other runtime data are created.

---

### Question

**Who frees memory in JavaScript?**

Answer:

The JavaScript Engine's Garbage Collector automatically reclaims memory occupied by objects that are no longer reachable.

---

### Question

**What is the difference between Stack and Heap?**

A concise answer:

> The Stack stores execution contexts and other short-lived execution data, while the Heap stores dynamically allocated objects and other complex data structures. The Heap is managed by the Garbage Collector.

---

# Common Mistakes

❌ Thinking JavaScript developers manually free memory.

❌ Assuming Garbage Collection happens immediately.

❌ Believing every object is removed as soon as a function ends.

❌ Confusing Stack Memory with Heap Memory.

❌ Assuming automatic memory management eliminates all memory leaks.

---

# Key Takeaways

- JavaScript automatically manages memory.
- Values are allocated memory when created.
- The Stack and Heap serve different purposes.
- The Garbage Collector reclaims memory that is no longer reachable.
- Memory leaks are still possible when references are unintentionally retained.
- Understanding memory management is essential for building performant Angular applications.

---

## Next Section

In **Section 12 — Angular Connection & Why JavaScript Engine Knowledge Matters**, we'll bring everything together and see how JavaScript Engine concepts directly influence Angular topics such as Change Detection, Signals, Zone.js, performance optimization, debugging, and interview discussions.

---

## Section 12 — Chapter Summary

Key takeaways.

---

# Estimated Reading Time

45–60 minutes

---

# Difficulty

⭐⭐☆☆☆ (Beginner to Intermediate)

---

# Angular Connection

Although Angular is a frontend framework, it does not execute JavaScript itself.

Every Angular component, service, directive, lifecycle hook, RxJS subscription, and event handler ultimately runs on the JavaScript engine provided by the execution environment.

Understanding the JavaScript engine will make it much easier to understand later topics such as:

- Change Detection
- Zone.js
- Signals
- Performance Optimization
- Memory Leaks
- RxJS Execution
- Browser Rendering

---

# What's Next?

The next section begins with:

> **Section 1 — Introduction to the JavaScript Engine**

where we'll answer one fundamental question:

**"What exactly is a JavaScript Engine?"**