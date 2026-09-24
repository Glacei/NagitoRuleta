import random
import customtkinter as ctk


class RouletteApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure the main application window and its responsive layout.
        self.title("RULETA CHUPI :D")
        self.geometry("520x560")
        self.minsize(420, 480)
        self.configure(fg_color="#10151d")
        self.is_spinning = False

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # The header gives the app its title and short description.
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=32, pady=(34, 0), sticky="ew")

        ctk.CTkLabel(
            header,
            text="CHUPI RULETA :D",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#f4f7fb",
        ).pack(anchor="w")
        ctk.CTkLabel(
            header,
            text="Pon un numero máximo y gl",
            font=ctk.CTkFont(size=14),
            text_color="#8f9baa",
        ).pack(anchor="w", pady=(5, 0))

        # This section lets the user choose the upper limit for the roulette.
        controls = ctk.CTkFrame(self, fg_color="#1a222d", corner_radius=14)
        controls.grid(row=1, column=0, padx=32, pady=28, sticky="ew")
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

        # The result panel displays the changing number while the roulette spins.
        result_frame = ctk.CTkFrame(self, fg_color="#182936", corner_radius=24)
        result_frame.grid(row=2, column=0, padx=32, pady=(0, 24), sticky="nsew")

        ctk.CTkLabel(
            result_frame,
            text="TU NÚMERO",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#79c8c0",
        ).pack(pady=(42, 5))

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

        self.spin_button = ctk.CTkButton(
            self,
            text="GIRAR RULETA",
            height=50,
            corner_radius=12,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#e56b52",
            hover_color="#c95741",
            command=self.spin,
        )
        self.spin_button.grid(row=3, column=0, padx=32, pady=(0, 34), sticky="ew")

    def spin(self):
        # Ignore extra clicks while an existing spin is still running.
        if self.is_spinning:
            return

        # Convert the input to an integer and reject zero, negatives, and text.
        try:
            maximum = int(self.maximum_input.get())
            if maximum < 1:
                raise ValueError
        except ValueError:
            self.status_label.configure(text="Introduce un número entero mayor que 0", text_color="#f09a83")
            self.maximum_input.focus_set()
            return

        # Lock the controls until the animated spin has finished.
        self.is_spinning = True
        self.spin_button.configure(state="disabled", text="GIRANDO...")
        self.maximum_input.configure(state="disabled")
        self.status_label.configure(text=f"Seleccionando un número del 1 al {maximum}...", text_color="#8f9baa")
        self.animate_spin(maximum, 0)

    def animate_spin(self, maximum, step):
        # Show a temporary random number to create the spinning effect.
        self.result_label.configure(text=str(random.randint(1, maximum)))
        if step < 18:
            # Schedule the next update without freezing the window.
            self.after(55 + step * 8, lambda: self.animate_spin(maximum, step + 1))
            return

        # Pick and display the final winning number.
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
        