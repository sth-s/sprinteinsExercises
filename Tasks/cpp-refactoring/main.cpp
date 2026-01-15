
#include <json/json.h>
#include <iostream>
#include <string>
#include <fstream>
#include <algorithm>
#include <math.h>

// install: jsoncpp http://macappstore.org/jsoncpp/
// to run: g++ -std=c++11  -L /usr/local/lib -ljsoncpp tamash.cpp -o tamash.o && ./tamash.o

using namespace std;

enum string_code
{
    tragedy,
    comedy,
    none
};

string_code hashit(std::string const &inString)
{
    if (inString == "tragedy")
    {
        return tragedy;
    }
    if (inString == "comedy")
    {
        return comedy;
    }
    else
    {
        return none;
    }
}

string statement(Json::Value &invoices, Json::Value &plays)
{
    unsigned int totalAmount{0};
    unsigned int volumeCredits{0};

    string result = "Statement for " + invoices[0]["customer"].asString() + " \n";
    Json::Value performances = invoices[0]["performances"];

    for (int index = 0; index < performances.size(); ++index)
    {
        unsigned int thisAmount{0};
        auto play = plays[performances[index]["playID"].asString()];
        int audience = performances[index]["audience"].asInt();

        switch (hashit(play["type"].asString()))
        {
        case tragedy:
            thisAmount = 40000;
            if (audience > 30)
            {
                thisAmount += 1000 * (audience - 30);
            }
            break;
        case comedy:
            thisAmount = 30000;
            if (audience > 20)
            {
                thisAmount += 10000 + 500 * (audience - 20);
            }
            thisAmount += 300 * audience;
            break;
        default:
            return "error";
        }

        volumeCredits += max(audience - 30, 0);

        if (play["type"].asString() == "comedy")
        {
            volumeCredits += floor(audience / 5);
        }

        result += " " + play["name"].asString() + ": $" + std::to_string(thisAmount / 100) + "(" + std::to_string(audience) + " seats)\n";
        totalAmount += thisAmount;
    }

    result += "Amount owed is $" + std::to_string(totalAmount / 100) + "\n";
    result += "You earned " + std::to_string(volumeCredits) + " credits\n";
    return result;
}

int main()
{
    ifstream playsFile("plays.json");
    ifstream invoicesFile("invoices.json");

    Json::Value plays;
    Json::Value invoices;

    playsFile >> plays;
    invoicesFile >> invoices;

    cout << statement(invoices, plays);

    return 0;
}