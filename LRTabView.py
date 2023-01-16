import customtkinter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error


class LRTabView:
    __tab_name = 'Linear Regression'

    @staticmethod
    def get_tab_name() -> str:
        return LRTabView.__tab_name

    def __init__(self, tab_view: customtkinter.CTkFrame):
        self.dataset_path = ''

        self.__dataset = pd.DataFrame()
        self.__regression_model = LinearRegression()
        self.__x_train: np.array = None
        self.__x_test: np.array = None
        self.__y_train: np.array = None
        self.__y_test: np.array = None
        self.__dependent_column = ''

        self.__tab_view = tab_view

        # Declaring widgets
        self.__predicted_value_label: customtkinter.CTkLabel
        self.__independent_feature_option_menu: customtkinter.CTkOptionMenu
        self.__feature_entry: customtkinter.CTkEntry
        self.__plot_graph_checkbox: customtkinter.CTkCheckBox

    def __invalidate_widgets(self):
        for widgets in self.__tab_view.winfo_children():
            widgets.destroy()

        self.__predicted_value_label = customtkinter.CTkLabel(self.__tab_view)
        self.__independent_feature_option_menu = customtkinter.CTkOptionMenu(self.__tab_view)
        self.__feature_entry = customtkinter.CTkEntry(self.__tab_view)
        self.__plot_graph_checkbox = customtkinter.CTkCheckBox(self.__tab_view)

    def __create_layout(self, dataset_path: str):
        self.dataset_path = dataset_path

        # import and process dataset
        self.__dataset = pd.read_csv(self.dataset_path)
        self.__dataset = self.__dataset.select_dtypes(include=np.number)
        self.__dataset.dropna(inplace=True)

        self.__dependent_column = self.__dataset.columns[-1]

        attribute_list = list(self.__dataset.columns.values)
        attribute_list.pop()
        self.__independent_feature_option_menu.configure(values=attribute_list, width=200, dynamic_resizing=False)
        self.__independent_feature_option_menu.set(attribute_list[0])
        self.__independent_feature_option_menu.grid(row=0, column=0, padx=10, pady=10)

        self.__feature_entry.configure(width=200, placeholder_text='Enter Value')
        self.__feature_entry.grid(row=0, column=1, padx=10, pady=10)

        self.__plot_graph_checkbox.configure(text='Plot Graph')
        self.__plot_graph_checkbox.grid(row=0, column=2, padx=10, pady=10)

    def __plot(self, column):
        if self.dataset_path != '':
            figure = plt.Figure(figsize=(6, 5))
            figure.set_layout_engine("constrained")
            ax = figure.subplots()

            y_predicted = self.__regression_model.predict(self.__x_test.reshape(-1, 1))
            scatter_df = pd.DataFrame(data={'X_Actual': self.__x_test, 'Y_Actual': self.__y_test})
            predicted_df = pd.DataFrame(data={'X_Actual': self.__x_test, 'Y_Predicted': y_predicted.ravel()})

            comparison_df = pd.DataFrame(data={'Y_Actual': self.__y_test, 'Y_Predicted': y_predicted.ravel()})
            y_difference = comparison_df.eval("Y_Predicted - Y_Actual").rename("Y_Difference")
            diff_range = min(abs(y_difference.min()), abs(y_difference.max()))

            sns.scatterplot(data=scatter_df, x='X_Actual', y='Y_Actual', ax=ax, hue='Y_Actual')
            ax.yaxis.set_label_position("right")

            sns.lineplot(data=predicted_df, x='X_Actual', y='Y_Predicted', ax=ax, color='orange')

            canvas = FigureCanvasTkAgg(figure, master=self.__tab_view)
            canvas.draw()
            canvas.get_tk_widget().grid(row=2, column=0, columnspan=3)

    def predict(self):
        # Training the model
        selected_column = self.__independent_feature_option_menu.get()
        x = self.__dataset[selected_column].values
        y = self.__dataset['Profit'].values

        self.__x_train, self.__x_test, self.__y_train, self.__y_test = train_test_split(x, y, test_size=0.3,
                                                                                        random_state=42)
        self.__regression_model.fit(self.__x_train.reshape(-1, 1), self.__y_train.reshape(-1, 1))
        predicted_value = self.__regression_model.predict(np.array(float(self.__feature_entry.get())).reshape(-1, 1))
        self.__predicted_value_label.configure(text=f'Predicted Profit is {predicted_value[0][0]}',
                                               font=customtkinter.CTkFont(size=20, weight="bold"))
        self.__predicted_value_label.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10), sticky='WE')

        if bool(self.__plot_graph_checkbox.get()):
            self.__plot(selected_column)

    def accuracy(self):
        predicted_values = self.__regression_model.predict(self.__x_test.reshape(-1, 1))
        mse = mean_squared_error(self.__y_test.reshape(-1, 1), predicted_values)
        rmse = np.sqrt(mse)
        r2score = r2_score(self.__y_test.reshape(-1, 1), predicted_values)
        print(f'Linear Regression: R2_Score: {r2score}, RMSE: {rmse}, MSE: {mse}')

    def invalidate(self, dataset_path: str):
        self.__invalidate_widgets()
        self.__create_layout(dataset_path)
