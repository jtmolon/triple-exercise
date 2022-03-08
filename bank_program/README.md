# Bank program evolution

# Task

The current django project has a simple architecture of part of the Triple internal business models. Triple as a loyalty
provider, has Programs, which represent specific cashback programs that run on Triple infrastructure; and has Banks
which provide the transactions to redeem in the cashback programs.

Programs give cashback in a currency, and Banks work by countries. With the current design, all programs will run in all
banks in all countries. We have noticed that the system has no limitation on which countries use what currencies. On
top of that, the business has requested we limit banks and programs combinations. So that we can say that Program1 is
only applicable to Bank1 in country GB.

The objective of this task is to implement a way to be able to check eligibility of incoming transactions by program, 
currency, country, and Bank. The code is left unstructured on purpose, the objective of the task is to organise the
code to have clear abstractions and implement things in a way that make sense in all layers.

The task should take around an hour if you are familiar with Django, and please, if you see that it's going to take too
long, describe the solution in text, explaining all the changes that would be done as well as the rationale behind some
key points.

# Developing

The project has been scaffolded with the default django project generator. A docker compose environment has been provided
for ease of development, and a Makefile is available with the most common actions.

To start, run `make api`, which should start the server locally.
