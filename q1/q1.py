import cv2
import numpy as np

# Defina seu RM aqui
RM = 95634

class VideoProcessor:
    def __init__(self, rm):
        self.video_path = self.escolher_video(rm)
        self.cap = cv2.VideoCapture(self.video_path)

    def escolher_video(self, rm):
        soma = sum(int(d) for d in str(rm))
        soma_final = sum(int(d) for d in str(soma))
        return "q1/q1A.mp4" if 1 <= soma_final <= 5 else "q1/q1B.mp4"

    def processar_frame(self, frame):
        # Seu código aqui.......
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(cv2.GaussianBlur(gray, (5, 5), 0), 60, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        maior_contorno = max(contours, key=cv2.contourArea, default=None)
        if maior_contorno is not None:
            x, y, w, h = cv2.boundingRect(maior_contorno)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            for c in contours:
                if c is not maior_contorno and cv2.pointPolygonTest(c, (x, y), False) >= 0:
                    cv2.putText(frame, "COLISÃO DETECTADA", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        return frame

    def executar(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            # Exibe resultado
            cv2.imshow("Feed", self.processar_frame(frame))
            if cv2.waitKey(1) & 0xFF == 27:
                break

        # That's how you exit
        self.cap.release()
        cv2.destroyAllWindows()

VideoProcessor(RM).executar()
