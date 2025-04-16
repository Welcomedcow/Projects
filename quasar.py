"""
Script to play a text-based version of Quasar from Mass Effect

The rules are explained in the specifications below.  For the optimal strategy to
maximize your winnings, see

    https://masseffect.fandom.com/wiki/Quasar

Author: Dustin Mercer
Date: Nov 30, 2024
"""
import random
random.seed(150)
import introcs


# Do not touch these first two functions. They are finished for you.
def prompt(prompt,valid):
    """
    Returns the choice from a given prompt.

    This function asks the user a question, and waits for a response.  It checks
    if the response is valid against a list of acceptable answers.  If it is not
    valid, it asks the question again. Otherwise, it returns the player's answer.

    Parameter prompt: The question prompt to display to the player
    Precondition: prompt is a string

    Parameter valid: The valid reponses
    Precondition: valid is a tuple of strings
    """
    # Ask the question for the first time.
    response = input(prompt)

    # Continue to ask while the response is not valid.
    while not (response in valid):
        print('Invalid option. Choose one of '+str(valid))
        print()
        response = input(prompt)

    return response


def payout(bet,score):
    """
    Returns the winnings for a game of quasar.

    Winnings are payout-bet.  So winning your bet (on a score of 17) has a net of 0.

    Parameter bet: the number of credits bet
    Precondition: bet is an int > 0

    Parameter score: the quasar score
    Precondition: score is an int >= 0
    """
    if score == 20:
        return bet
    elif score == 19:
        return round(0.5*bet)
    elif score == 18:
        return round(0.25*bet)
    elif score == 17:
        return 0
    elif score == 16:
        return round(-0.5*bet)
    elif score == 15:
        return round(-0.75*bet)

    # Everything else is a total loss
    return -bet


# Complete these functions
def get_bet(credits):
    """
    Returns the number of credits bet by the user.

    This function asks the user to make a bet

        Make a bet:

    If bet is not an integer, it responds with the error message

        The bet must be an integer.

    If bet is 0 or less, it responds with the error message

        The bet must be a positive integer.

    Finally, if bet is more than credits, it responds with the error message

        You do not have enough credits for that bet.

    It continues to ask for a bet until the user gives a valid answer.

    Parameter credits: the number of credits available to bet
    Precondition: credits is an int > 0
    """
    bet = 0
    halted = False
    while not halted:
        make_bet = input('Make a bet: ')
        if not introcs.isint(make_bet):
            print('The bet must be an integer.')
        elif int(make_bet) <= 0:
            print('The bet must be a positive integer.')
        elif int(make_bet) > credits:
            print('You do not have enough credits for that bet.')
        else:
            halted = True
            bet = int(make_bet)

    return int(bet)



def session(bet):
    """
    Returns the payout after playing a single session of quasar.

    The game starts by randomly choosing a number 1-8 and then displaying

        Your score is X.

    (where X is the number chosen). It then prompts the user with the following options:

        Choose (a) 4-7, (b) 1-8, or (s)top:

    If the user chooses 'a' or 'b', it picks a random number, adds it to the score,
    and then displays the score again.  If the user chooses 's' OR the new score is
    20 or more, the session is over.

    Once the session ends, if the user goes over 20, the function prints out

        You busted.

    However, if the user hits 20 exactly, the function prints out

        Quasar!

    Nothing extra is printed if the user is below 20.

    It then prints out

        You won X credits.

    or
        You lost X credits.

    as appropriate, where X is the payout (if X is 0, this is considered a win). When
    the session is done, the function returns the payout.

    Parameter bet: the number of credits bet
    Precondition: bet is an int > 0
    """
    score = random.randint(1,8)
    winnings = payout(bet,score)
    halted = False
    while not halted:
        print('Your score is '+str(score)+'.')
        question = prompt('Choose (a) 4-7, (b) 1-8, or (s)top: ',('a', 'b', 's'))
        if question == 'a':
            roll = random.randint(4,7)
            score += roll
            if score > 20:
                halted = True
                print('Your score is '+str(score)+'.')
                print('You busted.')
                winnings = payout(bet,score)
                if winnings >= 0:
                    print('You won '+str(winnings)+' credits.')
                else:
                    print('You lost '+str(winnings)+' credits.')
                halted = True
            elif score == 20:
                print('Quasar!')
                winnings = payout(bet,score)
                if winnings >= 0:
                    print('You won '+str(winnings)+' credits.')
                else:
                    print('You lost '+str(winnings)+' credits.')
                halted = True
        elif question == 'b':
            roll = random.randint(1,8)
            score += roll
            if score > 20:
                halted = True
                print('Your score is '+str(score)+'.')
                print('You busted.')
                winnings = payout(bet,score)
                if winnings >= 0:
                    print('You won '+str(winnings)+' credits.')
                else:
                    print('You lost '+str(winnings)+' credits.')
                halted = True
            elif score == 20:
                print('Quasar!')
                winnings = payout(bet,score)
                if winnings >= 0:
                    print('You won '+str(winnings)+' credits.')
                else:
                    print('You lost '+str(winnings)+' credits.')
                halted = True
        else:
            halted = True
            winnings = payout(bet,score)
            if winnings >= 0:
                print('You won '+str(winnings)+' credits.')
            else:
                print('You lost '+str(winnings)+' credits.')
    return winnings



def play(credits):
    """
    Plays Quasar until the player quits or is broke.

    The game starts by announcing

        You have X credits.

    where X is the number of credits.  It gets a bet from the user and plays a session
    of Quasar.  When done, it adds the payout to the score and repeats the message above.

    If the user reaches 0 credits, the game is over.  Otherwise, it asks

        Do you want to (c)ontinue or (p)ayout?

    If the user chooses 'c', the process repeats (get a bet, play a session, etc.)

    When done, the game prints

        You leave with X credits.

    assuming X > 0. However, if X is 0 it instead prints

        You went broke.

    Parameter credits: the number of credits available to bet
    Precondition: credits is an int > 0
    """
    halted = False
    while not halted:
        print('You have '+str(credits)+' credits.')
        bet = get_bet(credits)
        outcome = session(bet)
        credits += outcome
        print('You have '+str(credits)+' credits.')
        if credits > 0:
            question = prompt('Do you want to (c)ontinue or (p)ayout? ',('c', 'p'))
            halted = (question == 'p')
            if question == 'p':
                print('You leave with '+str(credits)+' credits.')
        else:
            credits <= 0
            halted = True
            print('You went broke.')



# Script Code
# DO NOT MODIFY BELOW THIS LINE
if __name__ == '__main__':
    play(1000)
