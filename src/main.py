import customtkinter
from RegressionApp import RegressionApp
from regression import Regression
from method_selection_widget import MethodSelectionWidget

if __name__ == '__main__':
    customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

    # widget = MethodSelectionWidget()
    # widget.mainloop()
    # methods = tuple([method for method, var in zip(Regression, widget.get_choices()) if var is True])
    methods = []

    print('Selected regression methods:', methods)

    app = RegressionApp(methods=methods)  # Possible Parameter: methods=(Regression.NeuralNetwork, Regression.MultipleLinear)
    app.mainloop()
