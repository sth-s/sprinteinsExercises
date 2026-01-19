def statement(invoice, plays):
    total_amount = 0
    volume_credits = 0
    result = f"Statement for {invoice['customer']}\n"

    def formatTheAmount(amount):
        return "${:,.2f}".format(amount / 100)

    for perf in invoice["performances"]:
        play = plays[perf["playID"]]
        this_amount = 0

        if play["type"] == "tragedy":
            this_amount = 40000
            if perf["audience"] > 30:
                this_amount += 1000 * (perf["audience"] - 30)
        elif play["type"] == "comedy":
            this_amount = 30000
            if perf["audience"] > 20:
                this_amount += 10000 + 500 * (perf["audience"] - 20)
            this_amount += 300 * perf["audience"]
        else:
            raise ValueError(f"unknown type: {play['type']}")

        # add volume credits
        volume_credits += max(perf["audience"] - 30, 0)

        # add extra credit for every ten comedy attendees
        if play["type"] == "comedy":
            volume_credits += perf["audience"] // 5

        # print line for this order
        result += f"  {play['name']}: {formatTheAmount(this_amount)} ({perf['audience']} seats)\n"
        total_amount += this_amount

    result += f"Amount owed is {formatTheAmount(total_amount)}\n"
    result += f"You earned {volume_credits} credits\n"
    return result
