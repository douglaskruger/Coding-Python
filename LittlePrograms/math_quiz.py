import random
import time
#https://gist.github.com/cwil323/9b1bfd25523f75d361879adfed550be2

def display_intro():
    title = "** A Simple Math Quiz **"
    print("*" * len(title))
    print(title)
    print("*" * len(title))

def get_name():
    user_name = input("What is your name? ")
    print("Good Luck", user_name, "!")
    return user_name

def get_num_questions():
    num_questions = int(input("How many questions shall we try? "))
    return num_questions

def display_menu():
    menu_list = ["  1. Addition", "  2. Subtraction", "  3. Multiplication", "  4. Integer Division", "  5. Exit"]
    print("Please choose the type of test")
    print(menu_list[0])
    print(menu_list[1])
    print(menu_list[2])
    print(menu_list[3])
    print(menu_list[4])


def display_separator():
    print("-" * 36)


def get_user_input():
    user_input = int(input("Enter your choice: "))
    while user_input > 5 or user_input <= 0:
        print("Invalid menu option.")
        user_input = int(input("Please try again: "))
    else:
        return user_input


def get_user_solution(problem):
    print(problem, end="")
    result = int(input(" = "))
    return result


def check_solution(user_solution, solution, count):
    if user_solution == solution:
        count = count + 1
        print("Correct.")
        print("")
        return count
    else:
        print("Incorrect. The answer is: ", solution)
        print("")
        return count


def menu_option(index, count):
    number_one = random.randrange(1, 21)
    number_two = random.randrange(1, 21)
    number_three = random.randrange(1, 10)
    number_four = random.randrange(1, 10)
    if index is 1:
        problem = str(number_one) + " + " + str(number_two)
        solution = number_one + number_two
        user_solution = get_user_solution(problem)
        count = check_solution(user_solution, solution, count)
        return count
    elif index is 2:
        problem = str(number_one) + " - " + str(number_two)
        solution = number_one - number_two
        user_solution = get_user_solution(problem)
        count = check_solution(user_solution, solution, count)
        return count
    elif index is 3:
        problem = str(number_three) + " * " + str(number_four)
        solution = number_three * number_four
        user_solution = get_user_solution(problem)
        count = check_solution(user_solution, solution, count)
        return count
    else:
        problem = str(number_three*number_four) + " / " + str(number_three)
        solution = number_four
        user_solution = get_user_solution(problem)
        count = check_solution(user_solution, solution, count)
        return count


def display_result(total, correct):
    if total > 0:
        result = correct / total
        percentage = round((result * 100), 2)
    if total == 0:
        percentage = 0
    print("You answered", total, "questions with", correct, "correct.")
    print("Your score is ", percentage, "%.", sep = "")


def main():
    display_intro()
    user_name = get_name()
    display_separator()
    display_menu()
    display_separator()
    option = get_user_input()
    display_separator()
    num_questions = get_num_questions()
    display_separator()
    total = 0
    correct = 0
    print("")
    start_time = time.time()
    while total < num_questions:
        total = total + 1
        print("Question:", total, " Enter your answer.")
        correct = menu_option(option, correct)

    elapsed_time = int(time.time() - start_time)
    print("Exit the quiz.")
    display_separator()
    display_result(total, correct)
    print("You took ", int(elapsed_time), " seconds. Average time per question =", elapsed_time/total, "seconds.")
    if correct / total > 0.8: 
        print("Good job -", user_name, "!")
    else:
        print("More practice needed ", user_name, "!")

main()
