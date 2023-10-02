from deepeval.metrics.metric import Metric
from deepeval.test_case import ImageTestCase
from ..singleton import Singleton


class ClipModel(metaclass=Singleton):
    def __init__(self, model_name="ViT-B/32"):
        self.model_name = model_name
        import torch
        import clip

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load(model_name, device=self.device)

    def get_similarity(self, image_path, query):
        import clip
        import torch
        from PIL import Image

        image_input = (
            self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
        )
        text_inputs = torch.cat([clip.tokenize(query)]).to(self.device)
        # Calculate features
        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
            text_features = self.model.encode_text(text_inputs)

        # Pick the top 5 most similar labels for the image
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
        score = float(similarity[0])
        return score


class ClipSimilarityMetric(Metric):
    def __init__(self, model_name="ViT-B/32", minimum_score: float = 0.3):
        self.clip_model = ClipModel(model_name)
        self.minimum_score = minimum_score

    def measure(self, test_case: ImageTestCase):
        score = self.clip_model.get_similarity(
            test_case.image_path, test_case.query
        )
        self.success = score > self.minimum_score
        return score

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "Clip Similarity"
