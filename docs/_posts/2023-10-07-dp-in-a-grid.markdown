---
layout: post
title:  "DP in a grid"
categories: DP, dynamic programming, C++
usemathjax: true
---

{% include math.html %}

This is an equation 
$$
x^2 + \ddot x = y(t)
$$

Background to our interest in DP.

Consider a maze, with _m_ rows and n columns

In each square of the maze, referred do by $$g(i, j)$$, we have a value - an integer value

We can also refer to individual squares using the notation (i, j) for the square at column i and row j

We want to minimize the cost of going from (0, 0) to (m-1, n-1)

In this variation of the problem, we can only move right and down.

This means that standing at a position (i, j), we can only move to (i+1, j) and (i, j+1), provided of course that the position that we move to is inside the maze

Introduce c(0, 0) as the sum of all m(i, j) when moving from (0, 0) to (i-1, j-1)

We want to compute min c(0, 0)

How can we do that?

We can generalize, and say that c(x, y) is the sum of all m(i, j) when moving from (x, y) to (i-1, j-1).

How can we compute min c(x, y)?

From (x, y) we can move to (x+1, y), or to (x, y+1)

Assuming we stay inside the maze, we could perhaps state that

min c(x, y) = min (m(x, y) + c(x+1, y), m(x, y) + c(x, y+1))

which we can simplify, as

min c(x, y) = m(x, y) + min (c(x+1, y), c(x, y+1))

This looks like something recursive

Can we make a function that computes this?

Yes, we can, but we need some boundary conditions.

We can call the boundary conditions base cases.

So we need some base cases.

What are these?

How about

c(i-1, j-1) = m(i-1, j-1)

Makes sense? Yes, it does.

What happens when x = i-1, i.e.

min c(i-1, y) = m(i-1, y) + min (c(i-1, y+1))

which becomes

min c(i-1, y) = m(i-1, y) + c(i-1, y+1))

which means that we can only move to the right

Similarly, when y = j-1, we can only move downwards, i.e.

min c(x, j-1) = m(x, j-1) + c(x+1, j-1)

This should be enough.

We can now construct a recursive function.

And we can add memoization.

This will be a top-down approach to dynamic programming.

What about a bottom-up approach?

Well, we could start with

c(i-1, j-1) = m(i-1, j-1)

Then we could move left, along the bottom row, using

min c(i-1, y) = m(i-1, y) + min (c(i-1, y+1))

And we could move up, along the rightmost column, using

min c(x, j-1) = m(x, j-1) + c(x+1, j-1)

Now we can start filling the rows, from right to left, starting with the next but last row and the next but last column, i.e. starting at position (m-2, n-2)

We do this using the original equation

min c(x, y) = m(x, y) + min (c(x+1, y), c(x, y+1))

This will work, since at a given position, the value to the right of us c(x, y+1) is known, and the value below us c(x+1, y) is also known.

I.e. we move to the right, or down, depending on which move gives the least cost.

Is there another way to do the bottom up approach?

What if we instead define c(x, y) as the cost of going from (0, 0) to (x, y).

We then want to minimize c(m-1, n-1)

We have

c(0, 0) = m(0, 0)

In the first row, we can only move right, so we must have

c(0, j) = m(0, j) + c(0, j-1)

In the first column, we can only move down, so we must have

c(i, 0) = m(i, 0) + c(i-1, 0)

Now we could fill in the rest, going right on each row, starting at the first row, at the second column, i.e. at (1, 1)

So we get

min c(x, y) = m(x, y) + min (c(x-1, y), c(x, y-1))

i.e we arrive at a position, either coming from the left or from above.

This looks really good. We could make a blog post of it. And refer to the Udemy course.

What if we can move arbitrarily?

What if there are obstacles, in the form of positions that we are not allowed to visit?

What if there are other constraints, such as we are not allowed to move twice in the same direction?

Let's do those in other blog posts.

All as a collection of ideas for Into Dynamic Programming.



