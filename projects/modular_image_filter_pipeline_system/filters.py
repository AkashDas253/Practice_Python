import cv2
import numpy as np

class FilterLibrary:
    @staticmethod
    def grayscale(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

    @staticmethod
    def blur(frame):
        return cv2.GaussianBlur(frame, (21, 21), 0)

    @staticmethod
    def edges(frame):
        edge = cv2.Canny(frame, 100, 200)
        return cv2.cvtColor(edge, cv2.COLOR_GRAY2RGB)

    @staticmethod
    def invert(frame):
        return cv2.bitwise_not(frame)

    @staticmethod
    def posterize(frame):
        n = 4 
        indices = np.arange(0, 256)
        divider = 256 / n
        quant = np.linspace(0, 255, n, dtype=np.uint8)
        idx = np.clip(np.int32(indices / divider), 0, n - 1)
        lookup_table = quant[idx]
        return cv2.LUT(frame, lookup_table)

    @staticmethod
    def sepia(frame):
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        sepia = cv2.transform(frame, kernel)
        return np.clip(sepia, 0, 255).astype(np.uint8)

    @staticmethod
    def thermal(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        thermal = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
        return cv2.cvtColor(thermal, cv2.COLOR_BGR2RGB)

    @staticmethod
    def sketch(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        inverted = 255 - gray
        blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blurred, scale=256)
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)

    @staticmethod
    def cartoon(frame):
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        blur = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                      cv2.THRESH_BINARY, 9, 2)
        edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        return cv2.bitwise_and(color, edges_rgb)

    @staticmethod
    def histogram_overlay(frame):
        h, w, _ = frame.shape
        overlay = frame.copy()
        cv2.rectangle(overlay, (w-220, h-120), (w-10, h-10), (0,0,0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        colors = ([255, 0, 0], [0, 255, 0], [0, 0, 255])
        for i, col in enumerate(colors):
            hist = cv2.calcHist([frame], [i], None, [256], [0, 256])
            cv2.normalize(hist, hist, 0, 100, cv2.NORM_MINMAX)
            points = np.int32(np.column_stack((
                np.linspace(w-210, w-20, 256), 
                h - 15 - hist
            )))
            cv2.polylines(frame, [points], False, col, 2)
        return frame

    @staticmethod
    def pixelate(frame):
        h, w = frame.shape[:2]
        temp = cv2.resize(frame, (w//16, h//16), interpolation=cv2.INTER_LINEAR)
        return cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)

    @staticmethod
    def sharpen(frame):
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        return cv2.filter2D(frame, -1, kernel)

    @staticmethod
    def hsv_shift(frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.float32)
        hsv[:, :, 0] = (hsv[:, :, 0] + 40) % 180
        hsv = hsv.astype(np.uint8)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

    @staticmethod
    def adaptive_threshold(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY, 11, 2)
        return cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)

    @staticmethod
    def emboss(frame):
        kernel = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        emboss = cv2.filter2D(gray, -1, kernel) + 128
        return cv2.cvtColor(emboss, cv2.COLOR_GRAY2RGB)