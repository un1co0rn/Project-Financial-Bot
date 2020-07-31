
import telebot
from telebot import types
from telebot.types import Message
from datetime import datetime
from pandas_datareader import data
import datetime
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.io import export_png
from bokeh.io.export import get_screenshot_as_png
from io import BytesIO

def status(close,open):
    if close > open:
        value = "Increase"
    elif open > close:
        value = "Decrease"
    else:
        value = "Same"
    return value

def get_graph(message: Message, input,days):
    # start = datetime.datetime(2018,3,1)
    start = datetime.datetime.now() - datetime.timedelta(days)
    end = datetime.datetime.now()

    print(start)
    try:
        # input = message.text


        data_frame = data.DataReader(name=input, data_source = "yahoo",start=start,end=end)
        data_frame["Status"] =  [status(close,open) for close,open in zip(data_frame.Close,data_frame.Open)]
        data_frame["Midle"] = (data_frame.Open + data_frame.Close)/2
        data_frame["Height"] = abs(data_frame.Open - data_frame.Close)




        plot = figure(x_axis_type = 'datetime', width=1000, height = 300,sizing_mode = "scale_width")
        plot.title.text = "%s Stocks CandleStick Chart" %(input)
        plot.grid.grid_line_alpha = 0.4

        hours_12 = 12*60*60*1000


        plot.segment(data_frame.index,data_frame.High, data_frame.index,data_frame.Low,color="black")

        plot.rect(data_frame.index[data_frame.Status == "Increase"],data_frame.Midle[data_frame.Status == "Increase"],hours_12,
         data_frame.Height[data_frame.Status == "Increase"],fill_color = "green", line_color = "black")

        plot.rect(data_frame.index[data_frame.Status == "Decrease"],data_frame.Midle[data_frame.Status == "Decrease"],hours_12,
         data_frame.Height[data_frame.Status == "Decrease"],fill_color = "red", line_color = "black")


        # conda install -c conda-forge phantomjs
        image = get_screenshot_as_png(plot, height=1000, width=1500)

        bio = BytesIO()
        bio.name = 'image.png'
        image.save(bio, 'PNG')
        bio.seek(0)
        bot.send_photo(message.chat.id, photo=bio)
        bot.send_message(message.chat.id, "Maximum price for a period: %s" %(data_frame.High.max()))
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id,"There`s no stock named like this")



bot = telebot.TeleBot("718189291:AAFtysih4mbfWSpF1NgVToVi1v6C_J363m0")


@bot.message_handler(content_types=['text'])
@bot.message_handler(commands=['start','reg','endSubscribe'])
def newSymbol(message: Message):
    if message.text == "/start":

        bot.send_message(message.chat.id,"Hi, write a symbol of market stock and take your graph!")
    else:
        global stock_name;
        stock_name = message.text
        print(input)
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="1 w", callback_data = "1w")
        btn2 = types.InlineKeyboardButton(text="1 m", callback_data = "1m")
        btn3 = types.InlineKeyboardButton(text="6 m", callback_data = "6m")
        btn4 = types.InlineKeyboardButton(text="1 y", callback_data = "1y")
        btn5 = types.InlineKeyboardButton(text="5 y", callback_data = "5y")
        keyboard.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id,"Hi, choose time graph!",reply_markup=keyboard)



            # output_file("png")
            # GOD BLESS YOURSELF AND MY FUTURE JOB
            # export_png(plot,filename="%s.png"%(input))



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "1w":
        bot.send_message(call.message.chat.id, "1w")
        print(stock_name)
        get_graph(call.message,stock_name,7)
    elif call.data == "1m":
        bot.send_message(call.message.chat.id, "1m")
        get_graph(call.message,stock_name,31)
    elif call.data == "6m":
        bot.send_message(call.message.chat.id, "6m")
        get_graph(call.message,stock_name,186)
    elif call.data == "1y":
        bot.send_message(call.message.chat.id, "1y")
        get_graph(call.message,stock_name,372)
    elif call.data == "5y":
        bot.send_message(call.message.chat.id, "5y")
        get_graph(call.message,stock_name,1860)






if __name__ == "__main__":
    try:
        bot.polling(none_stop = True)
    except:
        print("Oooops")
