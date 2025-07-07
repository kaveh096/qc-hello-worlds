# QC Hello Worlds

My repository for quantum computing resources and simple practices. My goal is to reach a point where I can solve realistic problems, not just understand quantum computing (QC) at a high level.

## Resources
<img src="qc_hello_worlds.png" alt="An illustration of a quantum computing learning journey" width="350" align="right" style="margin: 0 0 1em 2em;" />
As I learn QC, I will list my resources here for the benefit of others. I will focus only on free resources or material that is likely easily available to most people. The ones marked with a ✅ are those I have completed myself.

### Prerequisites

Material to review before diving into the other resources.

1.  ✅ **Linear Algebra**: You'll need to be comfortable with matrix algebra, determinants, traces, eigenvalues, etc. 3Blue1Brown [has a video series](https://www.3blue1brown.com/topics/linear-algebra) that I highly recommend.
2.  ✅ **Python**: There are countless resources to learn Python. I won't list them here. Just get comfortable with it.

### Quantum Mechanics

The first step is to learn (or re-learn) the fundamentals of Quantum Mechanics.

3.  **[The Feynman Lectures](https://www.feynmanlectures.caltech.edu/III_toc.html) on Physics, Vol. III**: A classic and insightful introduction to quantum mechanics by Richard Feynman..
4.  ✅ **Susskind's "The Theoretical Minimum"**: A book and [lecture series](https://theoreticalminimum.com/courses) by Leonard Susskind that aims to provide the essential knowledge for modern physics. The fact that this is freely available is baffling to me.
      * The [Quantum Mechanics course](https://theoreticalminimum.com/courses/quantum-mechanics/2012/winter) is a requirement, comprising approximately 20 hours of video lectures.
      * The rest are optional. I'm hooked and will likely continue.
5.  ✅ **Prompt Engineering**: I have put together [a prompt](prompts/physics_professor.md) (as a Gemini gem) so I can ask follow-up questions whenever I need to, and also to have AI quiz me. For example, as I'm watching Susskind lectures and encounter something I don't understand, I can have Gemini teach it to me and then quiz me. Feel free to customize it based on your own background and goals. Right now, it's instructed to ask you for those each time.

### Quantum Computing

Resources specifically for learning quantum computing (QC).

6.  ✅ [**QC for Beginners** on Coursera](https://www.coursera.org/specializations/packt-the-complete-quantum-computing-course-for-beginners): If you have access to Coursera via your school or work, this is a good resource. It covers the prerequisites (linear algebra, QM, Python) on its own. It doesn't delve too deeply into the math; you'll see some Dirac notation for circuits but not the proofs.
7.  [**QC course on Brilliant**](https://brilliant.org/courses/quantum-computing/): I haven't done it myself. Its outline seems similar to the one above, but it uses Q\# (Microsoft’s language) instead of Qiskit (IBM’s language).
8.  [**And more courses on Udemy**](https://www.udemy.com/topic/quantum-computing/).
9.  ✅ **3Blue1Brown video on Grover’s algorithm**: [Part 1](https://www.3blue1brown.com/lessons/grover), [Part 2](https://www.3blue1brown.com/lessons/grover-clarification). Whatever you do, don't skip this. It will give you a visual proof of Grover’s algorithm and also briefly explain what quantum computers could do in general.
10. If you want the proof for other famous quantum algorithms (like Shor’s), try the same prompt from item 5.
11. ✅ [**QC Gate Cheat Sheet**](https://docs.google.com/document/d/e/2PACX-1vTMarZzqZdT2k_nZi8rFl7poeQINyIKG4N6wEgnfyegg7WW2nI2GP9TLL61AnQqHnkDpcspJT-9ONAS/pub): A short document I prepared myself about all the QC gates and their definitions.
12. [**Qiskit Textbook**](https://qiskit.org/textbook/preface.html): An excellent open-source textbook that teaches the concepts of quantum computing from the ground up, with interactive code examples using IBM's Qiskit.
13. **"Quantum Computation and Quantum Information" by Nielsen & Chuang**: Often called the "bible" of quantum computing, this is the standard graduate-level textbook. Google it and you may find free PDFs.
14. **[Quantum Country](https://quantum.country)**: An interactive, mnemonic-based introduction to quantum computing and quantum mechanics. A great starting point for conceptual understanding. Co-authored by the same Michael Nielsen as above.
15. [**Quantum Computation video lecture from Umesh Vazirani**](https://www.youtube.com/watch?v=VPsl_5RQe1A&list=PLnhoxwUZN7-6hB2iWNhLrakuODLaxPTOG): This is a great lecture from Umesh Vazirani. This is next on my list.

### New Frontiers

Beyond learning QC fundamentals, I’d like to learn about practical ways to use them in the near future. So I will dig into Quantum AI, Quantum Approximate Optimization Algorithm (QAOA), etc.

16. [**k-SAT paper**](https://dl.acm.org/doi/10.1145/3313276.3316359): I've heard good things about this and need to read it.
17. ✅ I had Gemini compile [a comprehensive research on QAOA](https://docs.google.com/document/d/e/2PACX-1vSd7z9rS4XBRHQmrOw0_kQVcoeOYX8YADmTzWGbGhfKkbilnEHfFAe2GO7j36xnUqqhcth1Nc56rMcK/pub) from the web. Reading it should bootstrap you into the quantum approximation space.

### Further Material

18. I found a similar [QC resource list on GitHub](https://github.com/MonitSharma/Learn-Quantum-Computing-For-Free). It’s more exhaustive. If I find anything interesting there, I’ll cover it too.
