from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    And(Or(AKnave, AKnight), Not(And(AKnave, AKnight))),
    Implication(AKnave, Not(And(AKnave, AKnight))),
    Implication(AKnight, And(AKnight, AKnave)),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Implication(AKnave, Not(And(AKnave, BKnave))),
    And(Or(AKnave, AKnight), Not(And(AKnave, AKnight))),
    And(Or(BKnave, BKnight), Not(And(BKnave, BKnight))),
    Implication(AKnight, And(AKnave, AKnight))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Implication(AKnave, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))),
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    And(Or(AKnave, AKnight), Not(And(AKnave, AKnight))),
    And(Or(BKnave, BKnight), Not(And(BKnave, BKnight))),
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(BKnight, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    And(Or(AKnave, AKnight), Not(And(AKnave, AKnight))),
    And(Or(BKnave, BKnight), Not(And(BKnave, BKnight))),
    And(Or(CKnave, CKnight), Not(And(CKnave, CKnight))),
    Implication(BKnave, CKnight),
    Implication(BKnight, CKnave),
    Implication(CKnave, AKnave),
    Implication(CKnight, AKnight),
    Implication(AKnave,Not(Or(AKnight,AKnave))),
    Implication(AKnight,Or(AKnight,AKnave))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
