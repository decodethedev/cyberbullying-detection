import customtkinter
import pickle
import tensorflow as tf
import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from PIL import Image
from CTkMessagebox import CTkMessagebox

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def preprocess_text(text):
    if not text:
        return ""
    
    # Lowercase the text
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r"[^a-zA-Z]", " ", text)

    # Remove tags
    text = re.sub(r'@[\w_]+', '', text)

    # Tokenization
    tokens = nltk.word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    tokens = [word for word in tokens if word not in stop_words]

    # corrected_tokens = [spell.correction(word) for word in tokens]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens if word is not None]

    # Join the tokens back into a single string
    preprocessed_text = " ".join(lemmatized_tokens)

    return preprocessed_text

# Load the saved model
model = load_model("rnn_model3.h5")

# Load the tokenizer
with open("tokenizer3.pkl", "rb") as file:
    tokenizer = pickle.load(file)

def detect_cyberbullying(text):
    new_text = preprocess_text(text)
    new_text_seq = tokenizer.texts_to_sequences([new_text])
    max_sequence_length = 100
    new_text_padded = pad_sequences(new_text_seq, maxlen=max_sequence_length)

    # Make predictions
    predictions = model.predict(new_text_padded)

    # Convert the predictions to labels
    labels = ["toxic", "threat", "insult", "gender_hate", "religion_hate", "age_hate", "ethnicity_hate", "other_identity_hate"]
    predicted_labels = [labels[i] for i, prediction in enumerate(predictions[0]) if prediction >= 0.5]

    for i, prediction in enumerate(predictions[0]):
        print(f"{labels[i]}: {prediction*100}%")

    return predicted_labels

detect_cyberbullying("You are a stupid idiot") # Testing statement so that the model is loaded

class Comment(customtkinter.CTkFrame):
    def __init__(self, master, author, author_tag, text, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.author_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.author_frame.grid(row=0, column=0, sticky="ew")

        self.author_label = customtkinter.CTkLabel(self.author_frame, text=author, font=("Arial", 15, "bold"))
        self.author_label.grid(row=0, column=0, sticky="e")

        self.author_tag_label = customtkinter.CTkLabel(self.author_frame, text=author_tag, font=("Arial", 15, "italic"))
        self.author_tag_label.grid(row=0, column=1, padx=(5, 0))

        self.comment_text = customtkinter.CTkLabel(self, text=text, font=("Arial", 15), anchor="w")
        self.comment_text.grid(row=1, column=0, sticky="ew")
class PicturePostScenarioFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#292828", corner_radius=10)
        
        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(self, text="Picture Post Comments Scenario", font=("Arial", 20))
        self.label.grid(row=0, column=0, sticky="ew")

        self.container_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.container_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=20)

        self.post_frame = customtkinter.CTkFrame(self.container_frame)
        self.post_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        self.author_frame = customtkinter.CTkFrame(self.post_frame, fg_color="transparent")
        self.author_frame.grid(row=1, column=0, sticky="ew")

        self.author_label = customtkinter.CTkLabel(self.author_frame, text="SpongeBob Squarepants", font=("Arial", 15, "bold"))
        self.author_label.grid(row=0, column=0, sticky="e")

        self.author_tag_label = customtkinter.CTkLabel(self.author_frame, text="@spongebob", font=("Arial", 15, "italic"), width=100)
        self.author_tag_label.grid(row=0, column=1, padx=(5, 0))

        self.post_text = customtkinter.CTkLabel(self.post_frame, text="Currently chilling in Miami beach...", font=("Arial", 15), anchor="w")
        self.post_text.grid(row=2, column=0, sticky="ew")
        
        self.post_image = customtkinter.CTkImage(light_image=Image.open("spongebob.jpg"),
                                  dark_image=Image.open("spongebob.jpg"),
                                  size=(300, 300))
        self.post_image_holder = customtkinter.CTkLabel(self.post_frame, image=self.post_image, text=0)
        self.post_image_holder.grid(row=3, column=0, sticky="ew")

        self.comments_frame = customtkinter.CTkFrame(self.container_frame, width=600, corner_radius=20)
        self.comments_frame.grid(row=0, column=1, sticky="ew")

        comments_title = customtkinter.CTkLabel(self.comments_frame, text="Comments", font=("Arial", 20))
        comments_title.grid(row=0, column=0, sticky="ew")

        self.new_comment_frame = customtkinter.CTkScrollableFrame(self.comments_frame, fg_color="transparent", width=425, height=340)
        self.new_comment_frame.grid(row=1, column=0, sticky="nsew")
        
        comments = [
            {
                "author": "Patrick Star",
                "author_tag": "@patrick",
                "text": "I wish I was there too!"
            },
            {
                "author": "Squidward Tentacles",
                "author_tag": "@squidward",
                "text": "What's going on with your hand?"
            },
            {
                "author": "Mr. Krabs",
                "author_tag": "@krabs",
                "text": "Back to work!"
            },
        ]

        self.comment_count = 0
        
        for i in range(len(comments)):
            comment = comments[i]
            Comment(self.new_comment_frame, comment["author"], comment["author_tag"], comment["text"]).grid(row=i+1, column=0, sticky="ew", pady=10)
            self.comment_count += 1

        self.new_comment_post_frame = customtkinter.CTkFrame(self.comments_frame, )
        self.new_comment_post_frame.grid(row=2, column=0, sticky="ew", pady=10)
        self.columnconfigure(0, weight=1)

        self.mission = "MEAN"

        self.task = customtkinter.CTkLabel(self.new_comment_post_frame, text="Task: To test the model, say something really mean to him!", font=("Arial", 10))
        self.task.grid(row=0, column=0, sticky="ew")

        self.new_comment_variable = customtkinter.StringVar()

        self.new_comment_input = customtkinter.CTkEntry(self.new_comment_post_frame, width=410, corner_radius=0, textvariable=self.new_comment_variable)
        self.new_comment_input.grid(row=1, column=0, sticky="ew")

        self.new_comment_button = customtkinter.CTkButton(self.new_comment_post_frame, text="Post", width=10, corner_radius=0, command=self.post_new_comment)
        self.new_comment_button.grid(row=1, column=1, sticky="ew")

    def post_new_comment(self):
        text = self.new_comment_variable.get()

        if text == "":
            return
        
        predicted_labels = detect_cyberbullying(text)
        print(predicted_labels)

        # Use CTkMessagebox to display the predicted labels

        if len(predicted_labels) > 0:
            if self.mission == "MEAN":
                self.mission = "NICE"
                self.task.configure(text="Task: Say something nice to him!")

            CTkMessagebox(title="Cyberbullying Detected", message=f"The model has detected harmful content in your comment. Please try again. Harmful content types detected: {predicted_labels}. Your comment will not be sent and Spongebob won't see it.", icon="warning")
            return
        
        if self.mission == "MEAN":
            CTkMessagebox(title="Cyberbullying Not Detected", message="The task was to say something meanful to Spongbob so we can see it will protect Spongebob from meanful comments!", icon="info")
            return

        Comment(self.new_comment_frame, "You", "@you", text).grid(row=self.comment_count+1, column=0, sticky="ew", pady=10)
        self.comment_count += 1
class PrivateMessagesScenarioFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#292828", corner_radius=10)

        self.columnconfigure(0, weight=1)

        # Add old comments

        self.messages_frame = customtkinter.CTkFrame(self, width=600, corner_radius=20)
        self.messages_frame.grid(row=0, column=0, sticky="ew")

        customtkinter.CTkLabel(self.messages_frame, text="Private Messages", font=("Arial", 20)).grid(row=0, column=0, sticky="ew")

        self.messages_container = customtkinter.CTkScrollableFrame(self.messages_frame, fg_color="transparent", width=800, height=380)
        self.messages_container.grid(row=1, column=0, sticky="nsew")
        
        messages = [
            {
                "author": "SpongeBob SquarePants",
                "author_tag": "@spongebob",
                "text": "Hey, check out my new post, @you"
            },
            {
                "author": "SpongeBob SquarePants",
                "author_tag": "@spongebob",
                "text": "@you Do I look good? Please tell me because I need to know!"
            },
            {
                "author": "SpongeBob SquarePants",
                "author_tag": "@spongebob",
                "text": "Please repond, you are going to make me sad :("
            },
        ]

        self.messages_count = 0
        
        for i in range(len(messages)):
            msg = messages[i]
            Comment(self.messages_container, msg["author"], msg["author_tag"], msg["text"]).grid(row=i+1, column=0, sticky="ew", pady=10)
            self.messages_count += 1

        self.new_message_post_frame = customtkinter.CTkFrame(self, )
        self.new_message_post_frame.grid(row=1, column=0, sticky="ew", pady=10)

        self.mission = "MEAN"

        self.task = customtkinter.CTkLabel(self.new_message_post_frame, text="Task: To test the model, say something really mean to him!", font=("Arial", 10))
        self.task.grid(row=0, column=0, sticky="ew")

        self.new_message_variable = customtkinter.StringVar()

        self.new_message_input = customtkinter.CTkEntry(self.new_message_post_frame, width=780, corner_radius=0, textvariable=self.new_message_variable)
        self.new_message_input.grid(row=1, column=0, sticky="ew")

        self.new_message_button = customtkinter.CTkButton(self.new_message_post_frame, text="Post", width=10, corner_radius=0, command=self.new_message)
        self.new_message_button.grid(row=1, column=1, sticky="ew")\
        
    def new_message(self):
        text = self.new_message_variable.get()

        if text == "":
            return
        
        predicted_labels = detect_cyberbullying(text)
        print(predicted_labels)

        # Use CTkMessagebox to display the predicted labels
        if len(predicted_labels) > 0:
            if self.mission == "MEAN":
                self.mission = "NICE"
                self.task.configure(text="Task: Say something nice to him!")

            CTkMessagebox(title="Cyberbullying Detected", message=f"The model has detected harmful content in your message. Please try again. Harmful content types detected: {predicted_labels}. Your message will not be sent and Spongebob won't see it.", icon="warning")
            return
        
        if self.mission == "MEAN":
            CTkMessagebox(title="Cyberbullying Not Detected", message="The task was to say something meanful to Spongbob so we can see it will protect Spongebob from meanful messages!", icon="info")
            return
        
        Comment(self.messages_container, "You", "@you", text).grid(row=self.messages_count+1, column=0, sticky="ew", pady=10)
        self.messages_count += 1

class Post(customtkinter.CTkFrame):
    def __init__(self, master, author, author_tag, text, likes=0):
        super().__init__(master, fg_color="#292828", corner_radius=10)

        self.columnconfigure(0, weight=1)

        self.author = author
        self.author_tag = author_tag
        self.text = text

        self.author_label = customtkinter.CTkLabel(self, text=f"{author} {author_tag}", font=("Arial", 18))
        self.author_label.grid(row=0, column=0, sticky="w")

        self.text_label = customtkinter.CTkTextbox(self, font=("Arial", 15), width=400, height=100, corner_radius=10)
        self.text_label.grid(row=1, column=0, sticky="ew")

        self.text_label.insert("0.0", text)

        self.likes = likes

        self.like_button = customtkinter.CTkButton(self, text=f"Like ({likes})", width=10, corner_radius=0, command=self.like, fg_color="transparent")
        self.like_button.grid(row=2, column=0, sticky="ew")

    def like(self):
        self.likes += 1
        self.like_button.configure(text=f"Like ({self.likes})")
        

class HarrasmentPostScenarioFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#292828", corner_radius=10)

        self.columnconfigure(0, weight=1)

        self.title = customtkinter.CTkLabel(self, text="Harrasment Post Scenario", font=("Arial", 20))
        self.title.grid(row=0, column=0, sticky="ew")

        self.left_frame = customtkinter.CTkFrame(self)
        self.left_frame.grid(row=1, column=0, sticky="ew")

        self.task = customtkinter.CTkLabel(self.left_frame, text="Task: To test the model, make a post to talk mean stuffs to Spongebob", font=("Arial", 12))
        self.task.grid(row=1, column=0, sticky="ew")

        self.author_frame = customtkinter.CTkFrame(self.left_frame, fg_color="transparent")
        self.author_frame.grid(row=2, column=0, sticky="ew")

        self.author_label = customtkinter.CTkLabel(self.author_frame, text="You", font=("Arial", 15, "bold"))
        self.author_label.grid(row=0, column=0, sticky="e")

        self.author_tag_label = customtkinter.CTkLabel(self.author_frame, text="@you", font=("Arial", 15, "italic"))
        self.author_tag_label.grid(row=0, column=1, padx=(5, 0))

        self.mission = "MEAN"

        lbl = customtkinter.CTkLabel(self.left_frame, text="What's on your mind?", font=("Arial", 15), anchor="w")
        lbl.grid(row=3, column=0, sticky="ew")

        self.new_post_textbox = customtkinter.CTkTextbox(self.left_frame, height=100, width=400, corner_radius=0, font=("Arial", 16))
        self.new_post_textbox.grid(row=4, column=0, sticky="ew", pady=10)

        self.new_post_textbox.insert("0.0", "@spongebob ")

        customtkinter.CTkButton(self.left_frame, text="Post", corner_radius=0, command=self.new_post).grid(row=5, column=0, sticky="ew")

        self.right_frame = customtkinter.CTkFrame(self, height=500)
        self.right_frame.grid(row=1, column=1, sticky="ew")

        self.title = customtkinter.CTkLabel(self.right_frame, text="New Posts", font=("Arial", 20), fg_color="transparent")
        self.title.grid(row=0, column=0, sticky="ew")

        self.posts_container = customtkinter.CTkScrollableFrame(self.right_frame, fg_color="transparent", width=400, height=400)
        self.posts_container.grid(row=1, column=0, sticky="nsew")

        self.posts_count = 0

        posts = [
            {
                "author": "Spongebob",
                "author_tag": "@spongebob",
                "text": "My experience as a worker at the Krusty Krab has been great!",
                "likes": 24,
            },
            {
                "author": "Sandy",
                "author_tag": "@sandy",
                "text": "Anyone want to go to the beach with me?",
                "likes": 10,
            }
        ]

        for i in range(len(posts)):
            post = posts[i]
            Post(self.posts_container, post["author"], post["author_tag"], post["text"], post["likes"]).grid(row=i+1, column=0, sticky="ew", pady=10)
            self.posts_count += 1
        
    def new_post(self,):
        text = self.new_post_textbox.get("0.0", "end").strip()
        if text == "":
            return
        
        predicted_labels = detect_cyberbullying(text)
        
        if len(predicted_labels) > 0:
            if self.mission == "MEAN":
                self.mission = "NICE"
                self.task.configure(text="Task: Say something nice to him!")

            CTkMessagebox(title="Cyberbullying Detected", message=f"The model has detected harmful content in your post. Please try again. Harmful content types detected: {predicted_labels}. Your post will not be sent and Spongebob won't see it.", icon="warning")
            return
        
        if self.mission == "MEAN":
            CTkMessagebox(title="Cyberbullying Not Detected", message="The task was to post something meanful to Spongbob so we can see it will protect Spongebob from meanful posts!", icon="info")
            return

        self.posts_count += 1

        Post(self.posts_container, "You", "@you", text).grid(row=self.posts_count, column=0, sticky="ew", pady=10)

        self.new_post_textbox.delete("0.0", "end")
        self.new_post_textbox.insert("0.0", "@spongebob ")


class HowToUseFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#292828", corner_radius=10)

        self.label = customtkinter.CTkLabel(self, text="How to use this demo", font=("Arial", 20))
        self.label.grid(row=0, column=0, sticky="ew")
class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#292828", corner_radius=10)

        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(self, text="Home", font=("Arial", 20))
        self.label.grid(row=0, column=0, sticky="ew")

class TabButton(customtkinter.CTkButton):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, height=50, corner_radius=0, hover_color="#254dba", **kwargs)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cyberbullying Detection Demo Scenarios")
        self.geometry("1000x500")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.resizable(False, False)

        self.current_tab = None
        self.active_color = "#2e5bd9"

        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0, bg_color="#2c2f33")
        self.sidebar_frame.grid(row=0, column=0,  sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.title_label = customtkinter.CTkLabel(self.sidebar_frame, text="Demo Scenarios", font=("Arial", 20))
        self.title_label.grid(row=0, column=0, pady=(10,10), sticky="ew")

        self.home_tab_btn = TabButton(self.sidebar_frame, text="Home", command=lambda: self.show_tab("home"), fg_color=self.active_color)
        self.home_tab_btn.grid(row=1, column=0, sticky="ew")

        # self.how_to_use_tab_btn = TabButton(self.sidebar_frame, text="How to use this demo", command=lambda: self.show_tab("htu"), fg_color="transparent")
        # self.how_to_use_tab_btn.grid(row=2, column=0 , sticky="ew")

        self.picture_post_scenario_tab_btn = TabButton(self.sidebar_frame, text="Comments Scenario", command = lambda: self.show_tab("pps"), fg_color="transparent")
        self.picture_post_scenario_tab_btn.grid(row=3, column=0, sticky="ew")

        self.private_messages_scenario_tab_btn = TabButton(self.sidebar_frame, text="Private Messages Scenario", command = lambda: self.show_tab("pms"), fg_color="transparent")
        self.private_messages_scenario_tab_btn.grid(row=4, column=0, sticky="ew")

        self.harasment_post_scenario_tab_btn = TabButton(self.sidebar_frame, text="Harassment Post Scenario", command = lambda: self.show_tab("hps"), fg_color="transparent")
        self.harasment_post_scenario_tab_btn.grid(row=5, column=0, sticky="ew")
    
        # Tabs
        self.home_frame = HomeFrame(self)
        self.home_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # self.htu_frame = HowToUseFrame(self)
        self.pps_frame = PicturePostScenarioFrame(self)
        self.pms_frame = PrivateMessagesScenarioFrame(self)
        self.hps_frame = HarrasmentPostScenarioFrame(self)
    
    def show_tab(self, tab):
        if tab == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
            self.home_tab_btn.configure(fg_color=self.active_color)
        else:
            self.home_frame.grid_forget()
            self.home_tab_btn.configure(fg_color="transparent")
        
        # if tab == "htu":
        #     self.htu_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        #     self.how_to_use_tab_btn.configure(fg_color=self.active_color)
        # else:
        #     self.htu_frame.grid_forget()
        #     self.how_to_use_tab_btn.configure(fg_color="transparent")
        
        if tab == "pps":
            self.pps_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
            self.picture_post_scenario_tab_btn.configure(fg_color=self.active_color)
        else:
            self.pps_frame.grid_forget()
            self.picture_post_scenario_tab_btn.configure(fg_color="transparent")

        if tab == "pms":
            self.pms_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
            self.private_messages_scenario_tab_btn.configure(fg_color=self.active_color)
        else:
            self.pms_frame.grid_forget()
            self.private_messages_scenario_tab_btn.configure(fg_color="transparent")

        if tab == "hps":
            self.hps_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
            self.harasment_post_scenario_tab_btn.configure(fg_color=self.active_color)
        else:
            self.hps_frame.grid_forget()
            self.harasment_post_scenario_tab_btn.configure(fg_color="transparent")
        


app = App()
app.mainloop()