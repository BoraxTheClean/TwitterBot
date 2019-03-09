# State Classes

The game state must be completely serializable (Object->Bytes) and deserializable (Bytes->Object).

## Structure

Every _Game_ consists of one _Week_
Every _Week_ consists of a list of 7 _Days_
Every _Day_ consists of a list of 5 _Events_ (35 events)
Every _Event_ consists of a name and a _Poll_ (35 polls)
Every _Poll_ consists of a poll_text and 3 _PollOptions_ (105 PollOptions)
Every _PollOption_ consists of a option_text and a _PollOutcome_. (105 PollOutcomes)
Every _PollOutcome_ consists of the fundamental game attributes: socialness, sprintness, funocity, and careernosity, as well as payoff_text.

```
owencollierridge@penguin:~/git/TwitterBot/src$ cat json |grep -o Week|wc -l
1
owencollierridge@penguin:~/git/TwitterBot/src$ cat json |grep -o Day|wc -l
7
owencollierridge@penguin:~/git/TwitterBot/src$ cat json |grep -o Event|wc -l
35
owencollierridge@penguin:~/git/TwitterBot/src$ cat json |grep -o '\bPoll\b'|wc -l
35
owencollierridge@penguin:~/git/TwitterBot/src$ cat json |grep -o '\bPollOptions\b'|wc -l
105
owencollierridge@penguin:~/git/TwitterBot/src$ cat json |grep -o '\bPollOutcome\b'|wc -l
105
```
