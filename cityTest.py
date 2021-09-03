from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import csv
with open("worldcities.csv", newline='', encoding = 'UTF-8') as csvfile:
    data = csv.reader(csvfile, quoting=csv.QUOTE_ALL)

    def start(bot, update):
        update.message.reply_text("Cities game. If you want to stop enter /stop. You start)")


    def stop(bot, update, user_data):
        update.message.reply_text("Game over.")
        user_data.clear()



    def answer(update, user_data): #function to answer on user's city, user_data - dictionary with used cities, last character, number of used cities
        csvfile.seek(0)
        for row in data:
            ans = row[1].upper()
            if (ans[0] == user_data[-2] and (not (ans in user_data.values()))):
                update.message.reply_text(ans)
                user_data[-1] += 1
                user_data[user_data[-1]] = ans
                return ans[-1]#returns last character of answer

        update.message.reply_text("I'm lost")
        exit(0)


    def ansOnCity(bot, update, user_data): #handler function of entered word
        inp = update.message.text
        inp = inp.upper()
        if (not (len(user_data)==0) and inp[0] != user_data[-2]):
            update.message.reply_text("Enter city which begins on " + user_data[-2] + '\n')
        else:
            if (len(user_data) == 0):
                user_data[-1] = 0#number of used cities
                user_data[-2] = 'A'#last character of the last city
            hasans = False
            csvfile.seek(0)
            for row in data:
                ans = row[1].upper()
                if (inp == ans):
                    hasans = True
                    if (not (inp in user_data.values())):
                        user_data[-1] += 1
                        user_data[user_data[-1]] = inp
                        user_data[-2] = inp[-1]
                        user_data[-2] = answer(update, user_data)
                        break
                    else:
                        update.message.reply_text("This city was called")
                        break
            if not (hasans):
                update.message.reply_text("This city does not exist (or Bot doesn't know it)")



    updater = Updater("my token")

    disp = updater.dispatcher

    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(CommandHandler('stop', stop, pass_user_data=True))

    text = MessageHandler(Filters.text, ansOnCity, pass_user_data=True)

    disp.add_handler(text)

    updater.start_polling()

    updater.idle()


