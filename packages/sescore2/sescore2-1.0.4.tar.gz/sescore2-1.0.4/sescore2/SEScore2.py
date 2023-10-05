from .train.regression import *
from .downloader import download_from_drive
import os

class SEScore2:

    def __init__(self, lang):
        if not os.path.exists("sescore2_en_supervised_3B.ckpt"):
            download_from_drive()
        # load in the weights of SEScore2
        exp_config.device_id = torch.device("cpu") #torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        if lang == 'en':
            # load in english version
            self.tokenizer = AutoTokenizer.from_pretrained(f"google/mt5-xl")
            model_named_dict = torch.load('sescore2_en_supervised_3B.ckpt', map_location=torch.device('cpu'))
            # for key in list(model_named_dict.keys()):
            #    model_named_dict[key.replace('roberta.', '')] = model_named_dict.pop(key)

            hidden_size = 2048
            exp_config.hidden_size = hidden_size
            exp_config.hidden_size_FNN = [hidden_size * 2, hidden_size]
            self.model = Regression_XLM_Roberta(f"google/mt5-xl")

            self.model.load_state_dict(model_named_dict)  # .to(exp_config.device_id)
            self.model.to(exp_config.device_id)
            self.model.eval()
        elif lang == 'de':
            # load in german version
            self.tokenizer = AutoTokenizer.from_pretrained(f"google/rembert")
            self.model = torch.load('sescore2_de.ckpt').to(exp_config.device_id)
        elif lang == 'ja':
            # load in japanese version
            self.tokenizer = AutoTokenizer.from_pretrained(f"google/rembert")
            self.model = torch.load('sescore2_ja.ckpt').to(exp_config.device_id)
        elif lang == 'es':
            # load in spainish version
            self.tokenizer = AutoTokenizer.from_pretrained(f"google/rembert")
            self.model = torch.load('sescore2_es.ckpt').to(exp_config.device_id)
        elif lang == 'zh':
            # load in chinese version
            self.tokenizer = AutoTokenizer.from_pretrained(f"google/rembert")
            self.model = torch.load('sescore2_zh.ckpt').to(exp_config.device_id)
        else:
            print("We currently only support five languages: en, de, ja, es, zh!")
            exit(1)

        self.model.eval()

    def score(self, refs, outs, batch_size):
        scores_ls = []
        cur_data_dict = {'pivot': refs, 'mt': outs}
        cur_data_loader = preprocess_data(cur_data_dict, self.tokenizer, exp_config.max_length, batch_size,
                                          shuffle=False, sampler=False, mode='test')
        for batch in cur_data_loader:
            # generate a batch of ref, mt embeddings
            score = self.model(batch, 'last_layer').squeeze(1).tolist()
            scores_ls.extend(score)
        return scores_ls

# test the results 
# def main():
# refs = ["SEScore is a simple but effective next generation text generation evaluation metric", "SEScore it really works"]
# outs = ["SEScore is a simple effective text evaluation metric for next generation", "SEScore is not working"]
# refs = ["我是一个学生"]
# outs = ["老师是我"]

# scorer = SEScore2('zh')
# scores_ls = scorer.score(refs, outs, 1)
# print(scores_ls)

# if __name__ == "__main__":
#    main()
