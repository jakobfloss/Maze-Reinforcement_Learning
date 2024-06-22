---
marp: true
theme: uibk
paginate: true
# dont show page number on first slide
_paginate: skip
# header: test the header
footer: Data Science and Statistical Methods 2 \n Jakob Floss
---
# Solving a Maze - Reinforcement Learning

![test](../learning_animations/very_very_big_maze_lr0.1_er0.50.gif)

---
# Contents

* Reinforcement learning - Introduction
* Environment: Maze
* Agent: Roboter
* Reward system

---
# Reinforcement Learning

> **Reinforcement learning (RL)** is an interdisciplinary area of machine learning and optimal control concerned with how an <u>*intelligent agent*</u> ought to <u>*take actions in a dynamic environment*</u> in order to <u>*maximize the cumulative reward*</u>. Reinforcement learning is one of three basic machine learning paradigms, alongside supervised learning and unsupervised learning.
-- <cite>Wikipedia</cite>

---
# The Environment

* In our case: the maze
* Provides a system, with wich the agent can interact
* Stores:
  * Actual maze
  * Player position
* Provides to the agent:
  * Possible moves
  * Rewards


---
# Contents

<div class=columns>

<div>

## Reinforcement Learning

<br>

* Environment
<br>

* Agent
<br>

* Reward system
</div>

<div>

<!-- <h2 style="text-align: center"> Maze example </h2> -->
## Maze example

<br>

* asdf
<br>

* lfs
<br>

* asdf

</div>

</div>

---

# Reinforcment vs (Un)supervised Learning

<div class=columns>

<div>

## (Un)supervised
This is a text without a list
- Training set
  - with/without assigned features
</div>

<div>

## Reinforcement

</div>

</div>


---
# Multi columns in Marp slide

<div class="columns">
<div>

## Column 1

- item 1
  - subitem 1
- item 2

</div>
<div>

## Column 2

1. test
2. test
    1. test
3. test

</div>
</div>

---

# Multi columns in Marp slide

<div class="columns3">
<div>

## Column 1

Tempore ad exercitationem necessitatibus nulla, optio distinctio illo non similique?

</div>
<div>

## Column 2

Tempore ad exercitationem necessitatibus nulla, optio distinctio illo non similique?

</div>
<div>

## Column 3

Tempore ad exercitationem necessitatibus nulla, optio distinctio illo non similique?

</div>
</div>