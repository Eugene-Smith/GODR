import numpy as np
import cv2
import onnxruntime


def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

class StoneRecognizer():

    def __init__(self):
        self.model = onnxruntime.InferenceSession("src/models/model-2.onnx")

    def transform(self, img):
        img = img.astype(np.float32) / 255
        img = cv2.resize(img, dsize=(32, 32), interpolation=cv2.INTER_LINEAR)
        img = (img - 0.5) / 0.5
        img = np.expand_dims(img, axis=[0, 1])
        return img


    def recognize(self, img_gray, cell_size, intersections):
        CELL_SIZE_COEFF = 0.6

        delta = int(cell_size * CELL_SIZE_COEFF)
        white_stones = []
        black_stones = []
        for intersection in np.reshape(intersections, (-1, 2)):
            y = intersection[0]
            x = intersection[1]
            point_img = img_gray[max(x - delta, 0): min(x + delta, img_gray.shape[0]),
                                 max(y - delta, 0): min(y + delta, img_gray.shape[1])]
            data = self.transform(point_img)
            input = {self.model.get_inputs()[0].name: data}
            output = self.model.run(None, input)[0]
            pred = np.argmax(output, axis = 1)
            if pred == 0:
                white_stones.append(intersection)
            elif pred == 1:
                black_stones.append(intersection)
        return white_stones, black_stones
