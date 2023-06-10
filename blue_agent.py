import pandas as pd
import numpy as np
from ast import literal_eval
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

class Agent:
    def __init__(self, color, index):
        self.color = color
        self.index = index
        self.model = None

    def load_data(self, filename):
        # Load the data from the CSV file
        data = pd.read_csv(filename)

        # Convert string representation of lists to actual lists
        data['visible_world'] = data['visible_world'].apply(literal_eval)

        # Separate the features and target variable
        features = data.iloc[:, :-2]  # Select all columns except the last two (action and direction)
        target = data.iloc[:, -2:]  # Select the last two columns (action and direction)

        print("Features shape:", features.shape)
        print("Target shape:", target.shape)

        # Define a transformer to flatten and encode the visible_world column
        visible_world_transformer = ColumnTransformer(
            transformers=[('encoder', LabelEncoder(), [0])],
            remainder='passthrough'
        )

        print("ColumnTransformer configuration:")
        print(visible_world_transformer)

        # Define the pipeline
        pipeline = Pipeline([
            ('flatten_encode', visible_world_transformer),
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('classifier', DecisionTreeClassifier())
        ])

        # Train the model
        pipeline.fit(features, target)

        # Set the model
        self.model = pipeline

    def update(self, visible_world, position, can_shoot, holding_flag):
        # Prepare the input data for prediction
        input_data = pd.DataFrame({
            'visible_world': [visible_world],
            'position': [position],
            'can_shoot': [can_shoot],
            'holding_flag': [holding_flag]
        })

        # Make predictions using the trained model
        predictions = self.model.predict(input_data)

        # Extract the action and direction from the predictions
        action = predictions[0][0]
        direction = predictions[0][1]

        return action, direction

# Create an instance of the agent
agent = Agent(color="blue", index=0)

# Load the data from the CSV file
agent.load_data("data.csv")

# Example usage:
visible_world = [['x', 'x', 'x', 'x', 'x', '/', '/', 'x', '/']]
position = "(4, 8)"
can_shoot = True
holding_flag = None

action, direction = agent.update(visible_world, position, can_shoot, holding_flag)
print("Action:", action)
print("Direction:", direction)
