from dataclasses import dataclass
from random import randint
from drafter import *
from bakery import assert_equal
set_website_title("The Casino")
set_site_information(
    author="Andrew Arnold",
    description="A virtual casino that teaches people about gambling risks.",
    sources="Drafter documentation and gambling support websites.",
    planning=[],
    links=[]
)
hide_debug_information()
set_website_framed(False)
@dataclass
class GameRecord:
    game_name: str
    bet_amount: float
    result: str
    net_change: float
    balance_after: float
@dataclass
class State:
    balance: float
    college_fund_balance: float
    selected_game: str
    bet_amount: float
    total_wagered: float
    total_winnings: float
    total_losses: float
    game_history: list[GameRecord]
    used_college_fund: bool
    last_result: str
def initial_state(starting_money: float)->State:
    """Creates the starting state."""
    return State(starting_money, 500.0, "", 5.0, 0.0, 0.0, 0.0, [], False, "No games played yet.")
assert_equal(initial_state(100.0).balance, 100.0)
assert_equal(initial_state(50.0).balance, 50.0)
assert_equal(initial_state(200.0).balance, 200.0)
def prepare_bet(state: State, bet_amount: float, use_college_fund: bool)->bool:
    """Checks if the player has enough money."""
    if bet_amount <= 0:
        return False
    if state.balance <= 0 and use_college_fund:
        if state.used_college_fund == False:
            if bet_amount <= state.college_fund_balance:
                state.balance = state.college_fund_balance
                state.college_fund_balance = 0.0
                state.used_college_fund = True
    if bet_amount > state.balance:
        return False
    else:
        return True
assert_equal(prepare_bet(initial_state(100.0), 10.0, False), True)
assert_equal(prepare_bet(initial_state(100.0), 200.0, False), False)
assert_equal(prepare_bet(initial_state(100.0), -5.0, False), False)
def complete_round(state: State, game_name: str, bet_amount: float, won: bool, payout: float)->None:
    """Updates the money and saves the game result."""
    state.balance = round(state.balance - bet_amount + payout, 2)
    state.total_wagered += bet_amount
    if won:
        state.total_winnings += payout
        result = "Win"
        state.last_result = "🎉 You won $" + str(round(payout - bet_amount, 2))
    else:
        state.total_losses += bet_amount
        result = "Loss"
        state.last_result = "You lost $" + str(round(bet_amount, 2))
    change = payout - bet_amount
    game = GameRecord(game_name, bet_amount, result, change, state.balance)
    state.game_history.append(game)
state_test = initial_state(100.0)
complete_round(state_test, "Slots", 10.0, True, 40.0)
assert_equal(state_test.balance, 130.0)
assert_equal(state_test.total_wagered, 10.0)
assert_equal(len(state_test.game_history), 1)
@route
def index(state: State)->Page:
    """Shows the home page."""
    return Page(state, [
        Header("🎰 THE CASINO 🎰"),
        Header("PLAY - LEARN - BE AWARE"),
        Text("Welcome to your virtual casino!"),
        Header("💰 STARTING BALANCE: $100"),
        Text("Every player starts with $100 in fake money."),
        Text("Play slots or roulette and see how long your money lasts."),
        Text("Learn how gambling can affect your money."),
        Button("🎰 ENTER CASINO", "casino_lobby"),
        Button("❓ HELP AND INFORMATION", "help_page"),
        Text("⚠️ This simulation does not use real money.")
    ])
assert_equal(isinstance(index(initial_state(100.0)), Page), True)
assert_equal(isinstance(index(initial_state(50.0)), Page), True)
assert_equal(isinstance(index(initial_state(200.0)), Page), True)
@route
def casino_lobby(state: State)->Page:
    """Shows the casino lobby."""
    return Page(state, [
        Header("🎰 THE CASINO 🎰"),
        Header("CASINO LOBBY"),
        Header("💰 YOUR BALANCE"),
        Header("$" + str(round(state.balance, 2))),
        Header("🎮 CHOOSE YOUR GAME"),
        Header("🎰 SLOTS"),
        Text("20% chance to win."),
        Button("🎰 PLAY SLOTS", "slots_game"),
        Header("🎲 ROULETTE"),
        Text("47.37% chance to win."),
        Button("🎲 PLAY ROULETTE", "roulette_game"),
        Header("📊 YOUR STATS"),
        Text("Total Wagered: $" + str(round(state.total_wagered, 2))),
        Text("Rounds Played: " + str(len(state.game_history))),
        Button("💰 VIEW WALLET", "wallet_page"),
        Button("📋 FINAL REPORT", "final_report"),
        Button("GAME RULES", "game_rules"),
        Button("❓ HELP", "help_page")
    ])
assert_equal(isinstance(casino_lobby(initial_state(100.0)), Page), True)
assert_equal(isinstance(casino_lobby(initial_state(50.0)), Page), True)
assert_equal(isinstance(casino_lobby(initial_state(200.0)), Page), True)
@route
def game_rules(state: State)->Page:
    """Shows the rules and odds."""
    return Page(state, [
        Header("📖 GAME RULES"),
        Header("🎰 SLOTS"),
        Text("Chance to win: 20%"),
        Text("Chance to lose: 80%"),
        Text("House edge: 20%"),
        Text("Winning pays 4 times your bet."),
        Header("🎲 ROULETTE"),
        Text("Chance to win: 47.37%"),
        Text("Chance to lose: 52.63%"),
        Text("House edge: 5.26%"),
        Text("Choose red or black."),
        Text("Winning pays 2 times your bet."),
        Header("🏦 HOUSE EDGE"),
        Text("The casino has an advantage over time."),
        Text("Winning a few times does not guarantee profit."),
        Text("The more you bet, the more money you risk losing."),
        Button("⬅️ BACK TO LOBBY", "casino_lobby")
    ])
assert_equal(isinstance(game_rules(initial_state(100.0)), Page), True)
assert_equal(isinstance(game_rules(initial_state(50.0)), Page), True)
assert_equal(isinstance(game_rules(initial_state(200.0)), Page), True)
@route
def slots_game(state: State)->Page:
    """Shows the slots page."""
    state.selected_game = "Slots"
    return Page(state, [
        Header("🎰 SLOT MACHINE 🎰"),
        Header("💰 YOUR BALANCE"),
        Header("$" + str(round(state.balance, 2))),
        Header("777 - 777 - 777"),
        Text("Winning Chance: 20%"),
        Text("Winning Payout: 4x your bet"),
        Header("LAST RESULT"),
        Text(state.last_result),
        Header("PLACE YOUR BET"),
        Text("Enter your bet amount ($):"),
        TextBox("bet_amount", 5.0, "number"),
        Header("🎓 COLLEGE FUND"),
        Text("You have $500 saved for college."),
        Text("If you run out of money, you can choose to gamble with it."),
        Text("⚠️ You could lose money meant for school."),
        Text("Use college fund if balance is zero:"),
        CheckBox("use_college_fund"),
        Button("🎰 SPIN SLOTS", "play_slots"),
        Button("⬅️ BACK TO LOBBY", "casino_lobby")
    ])
state_test = initial_state(100.0)
assert_equal(isinstance(slots_game(state_test), Page), True)
assert_equal(state_test.selected_game, "Slots")
assert_equal(isinstance(slots_game(initial_state(50.0)), Page), True)
@route
def play_slots(state: State, bet_amount: float, use_college_fund: bool)->Page:
    """Plays one round of slots."""
    state.bet_amount = bet_amount
    if prepare_bet(state, bet_amount, use_college_fund):
        chance = randint(1, 100)
        if chance <= 20:
            won = True
            payout = bet_amount * 4
        else:
            won = False
            payout = 0.0
        complete_round(state, "Slots", bet_amount, won, payout)
    else:
        state.last_result = "⚠️ Invalid bet or not enough money."
    return slots_game(state)
state_test = initial_state(100.0)
play_slots(state_test, 5.0, False)
assert_equal(len(state_test.game_history), 1)
assert_equal(state_test.total_wagered, 5.0)
assert_equal(state_test.selected_game, "Slots")
@route
def roulette_game(state: State)->Page:
    """Shows the roulette page."""
    state.selected_game = "Roulette"
    return Page(state, [
        Header("🎲 ROULETTE 🎲"),
        Header("💰 YOUR BALANCE"),
        Header("$" + str(round(state.balance, 2))),
        Header("🔴 RED OR BLACK ⚫"),
        Text("Winning Chance: 47.37%"),
        Text("Winning Payout: 2x your bet"),
        Header("LAST RESULT"),
        Text(state.last_result),
        Header("PLACE YOUR BET"),
        Text("Enter your bet amount ($):"),
        TextBox("bet_amount", 5.0, "number"),
        Text("Choose your color:"),
        SelectBox("color", ["red", "black"], "red"),
        Header("🎓 COLLEGE FUND"),
        Text("You have $500 saved for college."),
        Text("You can use it if your balance reaches zero."),
        Text("⚠️ Remember that this money is meant for school."),
        Text("Use college fund if balance is zero:"),
        CheckBox("use_college_fund"),
        Button("🎲 SPIN ROULETTE", "play_roulette"),
        Button("⬅️ BACK TO LOBBY", "casino_lobby")
    ])
state_test = initial_state(100.0)
assert_equal(isinstance(roulette_game(state_test), Page), True)
assert_equal(state_test.selected_game, "Roulette")
assert_equal(isinstance(roulette_game(initial_state(50.0)), Page), True)
@route
def play_roulette(state: State, bet_amount: float, color: str, use_college_fund: bool)->Page:
    """Plays one round of roulette."""
    state.bet_amount = bet_amount
    if prepare_bet(state, bet_amount, use_college_fund):
        spin = randint(1, 38)
        if color == "red" and spin <= 18:
            won = True
        elif color == "black" and spin >= 19 and spin <= 36:
            won = True
        else:
            won = False
        if won:
            payout = bet_amount * 2
        else:
            payout = 0.0
        complete_round(state, "Roulette", bet_amount, won, payout)
    else:
        state.last_result = "⚠️ Invalid bet or not enough money."
    return roulette_game(state)
state_test = initial_state(100.0)
play_roulette(state_test, 5.0, "red", False)
assert_equal(len(state_test.game_history), 1)
assert_equal(state_test.total_wagered, 5.0)
assert_equal(state_test.selected_game, "Roulette")
@route
def wallet_page(state: State)->Page:
    """Shows the player's money and game history."""
    history = []
    for game in state.game_history:
        line = game.game_name + " | Bet: $" + str(round(game.bet_amount, 2))
        line += " | " + game.result
        line += " | Balance: $" + str(round(game.balance_after, 2))
        history.append(line)
    return Page(state, [
        Header("💰 YOUR WALLET"),
        Header("CURRENT BALANCE"),
        Header("$" + str(round(state.balance, 2))),
        Text("Starting Balance: $100"),
        Text("🎓 College Fund Remaining: $" + str(round(state.college_fund_balance, 2))),
        Header("📊 STATISTICS"),
        Text("Total Wagered: $" + str(round(state.total_wagered, 2))),
        Text("Total Payouts: $" + str(round(state.total_winnings, 2))),
        Text("Lost Bets: $" + str(round(state.total_losses, 2))),
        Text("Rounds Played: " + str(len(state.game_history))),
        Header("📜 GAME HISTORY"),
        BulletedList(history),
        Button("📋 FINAL REPORT", "final_report"),
        Button("⬅️ BACK TO LOBBY", "casino_lobby")
    ])
assert_equal(isinstance(wallet_page(initial_state(100.0)), Page), True)
assert_equal(isinstance(wallet_page(initial_state(50.0)), Page), True)
assert_equal(isinstance(wallet_page(initial_state(200.0)), Page), True)
@route
def final_report(state: State)->Page:
    """Shows the player's final results."""
    history = []
    for game in state.game_history:
        line = game.game_name + " | " + game.result
        line += " | Change: $" + str(round(game.net_change, 2))
        history.append(line)
    net_result = state.total_winnings - state.total_wagered
    return Page(state, [
        Header("📋 FINAL REPORT"),
        Header("YOUR RESULTS"),
        Text("Starting Balance: $100"),
        Header("💰 Final Balance: $" + str(round(state.balance, 2))),
        Text("Total Wagered: $" + str(round(state.total_wagered, 2))),
        Text("Total Payouts: $" + str(round(state.total_winnings, 2))),
        Text("Net Result: $" + str(round(net_result, 2))),
        Text("Total Rounds: " + str(len(state.game_history))),
        Header("📜 YOUR GAMES"),
        BulletedList(history),
        Header("⚠️ THE REALITY OF GAMBLING"),
        Text("The casino has an advantage over time."),
        Text("Winning streaks do not guarantee future wins."),
        Text("Gambling repeatedly can drain your money."),
        Text("Think about how much money you risked while playing."),
        Button("💰 VIEW WALLET", "wallet_page"),
        Button("⬅️ BACK TO LOBBY", "casino_lobby")
    ])
assert_equal(isinstance(final_report(initial_state(100.0)), Page), True)
assert_equal(isinstance(final_report(initial_state(50.0)), Page), True)
assert_equal(isinstance(final_report(initial_state(200.0)), Page), True)
@route
def help_page(state: State)->Page:
    """Shows gambling information and support resources."""
    return Page(state, [
        Header("❓ HELP AND INFORMATION"),
        Header("ABOUT THIS CASINO"),
        Text("This website uses fake money."),
        Text("No real money is involved."),
        Header("⚠️ GAMBLING RISKS"),
        Text("Casino games have a house advantage."),
        Text("Winning sometimes does not mean you will profit."),
        Text("Never gamble money needed for important expenses."),
        Text("Avoid chasing losses."),
        Header("🚨 WARNING SIGNS"),
        Text("Spending more money than you planned."),
        Text("Trying to win back money you lost."),
        Text("Gambling with money meant for bills or school."),
        Text("Having trouble stopping gambling."),
        Header("🤝 GAMBLING SUPPORT"),
        Text("If you or someone you know needs help, support is available."),
        Header("📞 NATIONAL PROBLEM GAMBLING HELPLINE"),
        Text("Call or text: 1-800-MY-RESET"),
        Text("Website: www.ncpgambling.org"),
        Header("📞 1-800-GAMBLER"),
        Text("Call: 1-800-426-2537"),
        Text("Website: www.1800gambler.net"),
        Header("GAMBLERS ANONYMOUS"),
        Text("Call: 855-222-5542"),
        Text("Website: gamblersanonymous.org"),
        Header("💙 REMEMBER"),
        Text("Asking for help is always an option."),
        Text("You do not have to deal with gambling problems alone."),
        Button("⬅️ BACK TO LOBBY", "casino_lobby")
    ])
assert_equal(isinstance(help_page(initial_state(100.0)), Page), True)
assert_equal(isinstance(help_page(initial_state(50.0)), Page), True)
assert_equal(isinstance(help_page(initial_state(200.0)), Page), True)
start_server(initial_state(100.0))
