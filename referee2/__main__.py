from referee2.main import main
win = 0
draw = 0
n = 100
for i in range(n):
    result = main()
    if result == "winner: upper":
        win += 1
    elif result == "winner: lower":
        win = win # do nothing lol
    else:
        draw += 1
    print("Game number " + str(i) + ": " + str(result))
        
print("upper win rate: " + str(win/(n-draw)))
print("upper wins: " + str(win))
print("lower wins: " + str(n-draw-win))
print("tie rate:" + str(draw/n))
print("ties: " + str(draw))

