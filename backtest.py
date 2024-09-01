from data import data_connector, process_data, signal_generators
from tests import profit_loss

my_p_l = profit_loss.p_l()
my_connector = data_connector.api_connector()
my_processor =process_data.processor()
my_sig_gens = signal_generators.sig_gens()

data = my_connector.yf_get(period=60)

formatted_data = my_processor.add_sma(data, [50,200])

#formatted_data = my_processor.format_columns(formatted_data)[0]
# yahoofinance already formats the columns with titles - doesnt need further formatting

signal = []
signal.append(0)
for i in range(1,len(formatted_data)):
    df = formatted_data[i-1:i+1]
    signal.append(my_sig_gens.og_sig_gen(df))
#og_signal_generator(data)

formatted_data["signal"] = signal

#formatted_data.to_csv("data.csv", index=False)

#print(formatted_data)

profit = my_p_l.calc_p_l(formatted_data)

print(profit)