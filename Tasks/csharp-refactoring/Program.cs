using System.ComponentModel.Design;
using System.Text.Json;

public class Program {

	public enum string_code 
	{
		tragedy, 
		comedy, 
		none
	}


	static string_code hashit(String inString) {
		if (inString.Equals("tragedy")) {
			return string_code.tragedy;
		}
		if (inString.Equals("comedy")) {
			return string_code.comedy;
		} else {
			return string_code.none;
		}
	}

	static String statement(JsonDocument invoices, JsonDocument plays) {

		int totalAmount = 0;
		int volumeCredits = 0;


		String result = "Statement for " + invoices.RootElement.EnumerateArray().First().GetProperty("customer").GetString() + " \n";
		var performances = invoices.RootElement.EnumerateArray().First().GetProperty("performances");

        foreach(var performance in performances.EnumerateArray())
        {
                    int thisAmount = 0;

                    var play = plays.RootElement.GetProperty(performance.GetProperty("playID").GetString());

                    int audience = performance.GetProperty("audience").GetInt32();

                    switch (((string_code)hashit(play.GetProperty("type").GetString()))) {
                        case string_code.tragedy:
                            thisAmount = 40000;
                            if (audience > 30) {
                                thisAmount += 1000 * (audience - 30);
                            }
                            break;
                        case string_code.comedy:
                            thisAmount = 30000;
                            if (audience > 20) {
                                thisAmount += 10000 + 500 * (audience - 20);
                            }
                            thisAmount += 300 * audience;
                            break;
                        default:
                            return "error";
                    }

                    // add volume credits
                    volumeCredits += Math.Max(audience - 30, 0);

                    // add extra credit for every ten comedy attendees
                    if (play.GetProperty("type").GetString() == "comedy")
                        volumeCredits += (int)Math.Floor((double)audience / 5.0d);

                    // print line for this order
                    result += " " + play.GetProperty("name").GetString() + ": $" + (thisAmount / 100) + "(" + audience + " seats)\n";
                    totalAmount += thisAmount;
        }


		result += "Amount owed is $" + (totalAmount / 100) + "\n";
		result += "You earned " + volumeCredits + " credits\n";
		return result;
	}

	static void Main(string[] args)
    {
		var playsFile = File.ReadAllText("plays.json");
		var invoicesFile = File.ReadAllText(("invoices.json"));

		var plays = JsonDocument.Parse(playsFile);

		var invoices = JsonDocument.Parse(invoicesFile);

		Console.WriteLine(statement(invoices, plays));
	}

}
