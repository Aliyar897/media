# from transformers import pipeline

from transformers import pipeline

# import logging
# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Singleton summarizer model
# class SummarizerModel:
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(SummarizerModel, cls).__new__(cls)
#             cls._instance.summarizer = summarizer = pipeline(
#                 "summarization", 
#                 model="facebook/bart-large-cnn",
#                 device=0
#             )
            
#         return cls._instance

# summarizer_model = SummarizerModel().summarizer

# import logging
# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Singleton summarizer model
# class SummarizerModel:
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(SummarizerModel, cls).__new__(cls)
#             cls._instance.summarizer = pipeline(
#                 "summarization", 
#                 model="sshleifer/distilbart-cnn-12-6", 
#                 revision="a4f8f3e", 
#                 device=0
#             )
#         return cls._instance

# summarizer_model = SummarizerModel().summarizer

# from transformers import pipeline
# # from .ai_model import summarizer_model


# # Function to split text into chunks
# def chunk_text(text, chunk_size, overlap_size):
#     for i in range(0, len(text), chunk_size - overlap_size):
#         yield text[i:i + chunk_size]


# import logging
# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def summarize(text):
#     logger.info('Summarizing text.......')
#     chunk_size = 500  # Reduce chunk size to control summary length
#     overlap_size = 50  # Adjust overlap size accordingly
#     summarized_text = []
    
#     for chunk in chunk_text(text, chunk_size, overlap_size):
#         try:
#             input_length = len(chunk.split())
#             max_length = min(150, input_length)
#             min_length = max(100, max_length - 50)  # Ensure min_length is reasonable
            
#             summarized_chunk = summarizer_model(
#                 chunk, 
#                 min_length=min_length,  # Ensure minimum length is reasonable
#                 max_length=max_length    # Ensure maximum length is within limits
#             )
#             summarized_text.append(summarized_chunk[0]['summary_text'])
#         except Exception as e:
#             logger.error(f"Error during summarization: {e}")
#             summarized_text.append(chunk)  # Fallback to original chunk
    
#     final_summary = ' '.join(summarized_text)
    
#     # Post-process to enforce length limits
#     summary_words = final_summary.split()
#     if len(summary_words) > 150:
#         final_summary = ' '.join(summary_words[:150])
#     elif len(summary_words) < 100:
#         final_summary = ' '.join(summary_words + ['...'] * (100 - len(summary_words)))

#     return final_summary


# text = "There are increasing signs that degeneration has set in, with the capability to deliver on the social contract between the citizenry and the rulers compromised . The country is teetering on the brink of financial insolvency, as the economy is hard-pressed to bear the burden of a bloated, predatory and extractive state machinery and its key functionaries’ lavish perks and privileges . The privileged segments, state functionaries and those well-connected with decision-makers have arrogated to the privileged segments . There is a deepening sense of vulnerability due to growing terrorism, the nature of the governing class, and the failure of administrative governance . The gap between diminishing state capability and the challenges being faced makes the task formidable . Civilian institutions, which serve as pillars on which the structure of the state rests, are largely dysfunctional Civilian institutions are largely dysfunctional . People are not able to participate freely, openly and transparently in the political process, and are also hurt by the absence of the rule of law . The institutions are fragile, with a disempowered executive, an inadequately functioning bureaucracy with limited capability, a rubber-stamping parliament, and a judiciary unable to operate a grievance redressal system, especially against the state . The growing gap between state capability and challenges has made the task formidable . Political and establishment interference, mismanagement, non-merited appointments to decision-making positions driven by a culture of loyalty and patronage, sheer incompetence as an incompetence . All of them suffer from a lack of internal stability and unity, having depleted their professional independence . The challenge is how to remedy this situation by making these institutions ‘normal’ through orderliness, harmony, and consistency . A rational view of engagement with the world is missing, while harbouring a victim syndrome, we also entertain an exaggerated view of our own importance . In the past, this assessment was fed by fortuitous global events, coupled with an institutionally ingrained belief that the establishment was better equipped to address the country’s multifarious challenges,  and self-serving definitions of national interest . It is difficult for the vast majority of the labour force, with limited education and skills, to participate meaningfully in the modern economy . The education and skill development systems have failed to enable this participation . Even university education is not producing knowledge and skill — nor the ability to acquire it — to meet the market demands of an economy growing at barely 2.5-3 per cent . The latest Labour Force Survey reveals that 31pc of graduates are unemployed and 34pc of 15-to-29-year olds have simply dropped out of the la la . 31pc of graduates are unemployed and 34pc of 15-to-29-year olds have simply dropped out of the labour force . Social indicators have not been allocated adequate funds for investments and operational spending . Education and health spending on education and health was 1.7pc of GDP in the 1980s, 3pc in the 1990s and 2.3pc in 2000s, the comparatives for defence have been 6.5% of GDP . To their credit, they deployed resources to create and embed a culture of discipline and internal cohesion . The economy is not growing at a pace to absorb the high population growth rate . But thanks to the internet and cable television, the youth is exposed to global developments, magnifying the challenges of managing expectations . The state’s huge footprint on the economy distorts markets, blocks opportunities and raises the cost of doing business through excessive, obsolete and flawed regulations . All this is presided over by a generalist, cadre-dominated civil service with a 19th-century mindset . A highly protected industrial structure is producing low productivity and low value-added goods . The economy’s competitiveness is being eroded by a power sector beleaguered by poorly negotiated contracts, incompetence and misgovernance . There is deep-seated mistrust between Islamabad and the smaller provinces, widening regional disparities in growth rates, quality of physical infrastructure and social and economic services have contributed to ethnic and intercommunal strains and stresses . Even the much-referred to monolithic category of the youth as an emerging vocal stakeholder is alienated along national/ ethnic/ values lines, with little by way of a sense of shared identity . Social divides are deepening, the space for talks is narrowing and hampering possibilities of coexistence, which is critical to social cohesion . Social cohesion built around a set of values requires a holistic approach to our sociopolitical and economic affairs. It needs reconfiguration of state and society. This is a huge challenge. Tackling it would be overwhelming for the most capable leadership anywhere in the world. And what are we blessed with? Subsequent articles on the key issues will be published . The writer is a former governor of the State Bank of Pakistan . e leadership anywhere in the world. And what are we blessed with? Subsequent articles on the key issues will attempt to propose the structures, policy actions, instruments, and institutional arrangements on the way forward. e leadership in Pakistan is the answer to the question: What do we have in leadership? And what do we really have? e leadership? e writes in an open letter to the author of this article . The author is also a former Governor of Pakistan's State Bank ."
# summary = summarize(text)
# # Print the character length
# print("Character length of original text:", len(text))
# print("Character length of summary:", len(summary))

# # Calculate and print the word count
# text_word_count = len(text.split())
# summary_word_count = len(summary.split())

# print("Word count of original text:", text_word_count)
# print("Word count of summary:", summary_word_count)
import logging
from transformers import BartForConditionalGeneration, BartTokenizer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Singleton summarizer model
class SummarizerModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SummarizerModel, cls).__new__(cls)
            cls._instance.tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
            cls._instance.model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
        return cls._instance

summarizer_instance = SummarizerModel()

# Function to summarize text
def summarize(text):
    print('Starting sumarization...', text)
    
    try:
        inputs = summarizer_instance.tokenizer(text, max_length=1024, return_tensors="pt", truncation=True)
        summary_ids = summarizer_instance.model.generate(
            inputs["input_ids"], 
            num_beams=4, 
            max_length=150, 
            early_stopping=True
        )
        summary = summarizer_instance.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    
    except Exception as e:
        logger.error(f"Error during summarization: {e}")
        return text  # Fallback to the original text if an error occurs