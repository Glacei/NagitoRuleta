import random
from pathlib import Path

import customtkinter as ctk
from PIL import Image


class RouletteApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("RULETA CHUPI :D")
        self.geometry("800x760")
        self.minsize(680, 640)
        self.configure(fg_color="#10151d")
        self.is_spinning = False

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # El header ocupa toda la parte superior y deja el titulo separado del contenido.
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=16, pady=(22, 14), sticky="ew")
        ctk.CTkLabel(
            header,
            text="CHUPI RULETA :D",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#f4f7fb",
        ).pack()
        ctk.CTkLabel(
            header,
            text="Pon un numero máximo y gl",
            font=ctk.CTkFont(size=14),
            text_color="#8f9baa",
        ).pack(pady=(5, 0))

        # El contenido principal coloca la ruleta a la izquierda y la imagen a la derecha.
        content = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame = content
        content.grid(row=1, column=0, padx=0, pady=(0, 12), sticky="nsew")
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)
        content.grid_rowconfigure(1, weight=1)

        # Seccion donde se le deja al usuario elegir el maximo numero que puede salir en la ruleta.
        controls = ctk.CTkFrame(content, fg_color="#1a222d", corner_radius=14)
        controls.grid(row=0, column=0, padx=(16, 8), pady=(0, 10), sticky="ew")
        controls.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            controls,
            text="NUMERO MÁXIMO",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#8f9baa",
        ).grid(row=0, column=0, padx=18, pady=(16, 5), sticky="w")

        self.maximum_input = ctk.CTkEntry(
            controls,
            placeholder_text="Por ejemplo, 15",
            height=42,
            font=ctk.CTkFont(size=15),
        )
        self.maximum_input.insert(0, "15")
        self.maximum_input.grid(row=1, column=0, padx=18, pady=(0, 16), sticky="ew")
        self.maximum_input.bind("<Return>", lambda _event: self.spin())

        # El panel del resultado te enseña numeros a lo random para dar la sensacion de ruleta y luego muestra el numero ganador.
        result_frame = ctk.CTkFrame(content, fg_color="#182936", corner_radius=24)
        result_frame.grid(row=1, column=0, padx=(16, 8), pady=(0, 10), sticky="nsew")

        ctk.CTkLabel(
            result_frame,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#79c8c0",
            text="TU NÚMERO",
        ).pack(pady=(24, 5))

        self.result_label = ctk.CTkLabel(
            result_frame,
            text="?",
            font=ctk.CTkFont(size=92, weight="bold"),
            text_color="#f4f7fb",
        )
        self.result_label.pack(expand=True)

        self.status_label = ctk.CTkLabel(
            result_frame,
            text="Listo para girar",
            font=ctk.CTkFont(size=14),
            text_color="#8f9baa",
        )
        self.status_label.pack(pady=(0, 38))

        # Carga la imagen y la alinea abajo en la columna derecha.
        image_path = Path(__file__).parent / "images" / "nagito.png"
        self.character_source_image = Image.open(image_path)
        self.character_image = ctk.CTkImage(
            light_image=self.character_source_image,
            dark_image=self.character_source_image,
            size=(1, 1),
        )
        self.character_label = ctk.CTkLabel(content, image=self.character_image, text="")
        self.character_label.grid(
            row=0, column=1, rowspan=3, padx=0, pady=0, sticky="s"
        )
        self.bind("<Configure>", self.resize_character_image)

        self.spin_button = ctk.CTkButton(
            content,
            text="GIRAR RULETA",
            height=50,
            corner_radius=12,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#e56b52",
            hover_color="#c95741",
            command=self.spin,
        )
        self.spin_button.grid(row=2, column=0, padx=(16, 8), sticky="ew")

    def resize_character_image(self, _event=None):
        # Espera a que Tk termine de recolocar los widgets antes de medirlos.
        self.after_idle(self._apply_character_image_size)

    def _apply_character_image_size(self):
        # Ajusta la imagen a la seccion inferior sin deformar sus proporciones.
        image_ratio = self.character_source_image.height / self.character_source_image.width
        available_width = max(1, int(self.winfo_width() * 0.32))
        image_width = available_width
        image_height = int(image_width * image_ratio)
        image_size = (image_width, image_height)

        if image_size != self.character_image.cget("size"):
            self.character_image.configure(size=image_size)

    def spin(self):
        # Ignora los clics mientras la ruleta esta girando.
        if self.is_spinning:
            return

        # Convierte el input puesto en un integer y valida que sea mayor que 0. Si no lo es, muestra un mensaje de error.
        try:
            maximum = int(self.maximum_input.get())
            if maximum < 1:
                raise ValueError
        except ValueError:
            self.status_label.configure(text="Introduce un número entero mayor que 0", text_color="#f09a83")
            self.maximum_input.focus_set()
            return

        # Bloquea los controles hasta que acabe la animacion.
        self.is_spinning = True
        self.spin_button.configure(state="disabled", text="GIRANDO...")
        self.maximum_input.configure(state="disabled")
        self.status_label.configure(text=f"Seleccionando un número del 1 al {maximum}...", text_color="#8f9baa")
        self.animate_spin(maximum, 0)

    def animate_spin(self, maximum, step):
        # Muestra un número aleatorio temporal para crear el efecto de giro.
        self.result_label.configure(text=str(random.randint(1, maximum)))
        if step < 18:
            # Programa la próxima actualización sin congelar la ventana.
            self.after(55 + step * 8, lambda: self.animate_spin(maximum, step + 1))
            return

        # Elige y muestra el numero ganador.
        winner = random.randint(1, maximum)
        self.result_label.configure(text=str(winner))
        self.status_label.configure(text=f"El número ganador es {winner}", text_color="#79c8c0")
        self.spin_button.configure(state="normal", text="GIRAR DE NUEVO")
        self.maximum_input.configure(state="normal")
        self.is_spinning = False


if __name__ == "__main__":
    # Start the application only when this file is run directly.
    app = RouletteApp()
    app.mainloop()
        