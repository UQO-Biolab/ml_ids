#wget http://kdd.ics.uci.edu/databases/kddcup99/kddcup.data.gz
#wget http://kdd.ics.uci.edu/databases/kddcup99/corrected.gz
#wget http://kdd.ics.uci.edu/databases/kddcup99/kddcup.names
#gzip -d /content/kddcup.data.gz
#gzip -d /content/corrected.gz

#pip install torch pandas matplotlib scikit-learn numpy

import pandas as pd
# reading the training data file
df = pd.read_csv("kddcup.data", header=None)
# reading the file containing feature names
with open("kddcup.names", 'r') as txt_file:
    col_names = txt_file.readlines()
col_names_cleaned = [i.split(':')[0] for i in col_names[1:]]
# adding an extra column for the indicator
col_names_cleaned.extend(['result'])
df.columns = col_names_cleaned
df.head()

import matplotlib.pyplot as plt
df['result'].value_counts().plot(kind='bar', figsize=(6, 3))
plt.suptitle('Distribution of Result Column -  Complete data ')
plt.show()
df_http = df[df.service == 'http']
df_http['result'].value_counts().plot(kind='bar', figsize=(6, 3))
plt.suptitle('Distribution of Result Column - "Service: http"')
plt.show()

import torch
import torch.nn as nn
import torch.optim as optim
# modele d'autoencoder
class VAE(nn.Module):
    def __init__(self):
        super(VAE, self).__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Linear(28, 14),
            nn.ReLU(),
            nn.Linear(14, 7)
        )
        self.mu_layer = nn.Linear(7, 2)
        self.logvar_layer = nn.Linear(7, 2)
        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(2, 7),
            nn.ReLU(),
            nn.Linear(7, 14),
            nn.ReLU(),
            nn.Linear(14, 28)
        )
    def encode(self, x):
        h = self.encoder(x)
        mu = self.mu_layer(h)
        logvar = self.logvar_layer(h)
        return mu, logvar
    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std
    def decode(self, z):
        return self.decoder(z)
    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        return self.decode(z), mu, logvar
# fonction de perte
def loss_function(recon_x, x, mu, logvar):
    MSE = nn.functional.mse_loss(recon_x, x)
    KLD = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return MSE + KLD
device = "cuda" if torch.cuda.is_available() else "cpu"
# initialisation / fonction de perte / opti
model_vae = VAE()
model_vae.to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model_vae.parameters(), lr=0.001)
# entrainement
num_epochs = 5
for epoch in range(num_epochs):
    for index, (inputs, labels) in enumerate(dataloader):
        inputs, labels = inputs.to(device), labels.to(device)
        recon, mu, logvar = model_vae(inputs)
        loss = loss_function(recon, inputs, mu, logvar)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if index%1000 == 0:
          print(f'Epoch [{epoch+1}/{num_epochs}], Iteration {index}, Loss: {loss.item():.4f}')
print("Training complete!")
from sklearn.metrics import precision_score, recall_score
import numpy as np
with torch.no_grad():
  X_scaled_test_recon, _, _ = model_vae(X_scaled_test.to(device))
loss_test = torch.nn.functional.mse_loss(X_scaled_test_recon.to(device), X_scaled_test.to(device), reduction='none').sum(1).cpu().numpy()
# fonction de perte
loss_test = loss_test - loss_test.min()
loss_test = loss_test/(loss_test.max())
predictions = (loss_test > 0.005).astype(np.int64)
# calcule la precision et le recalll
precision = precision_score(target, predictions )
recall = recall_score(target, predictions )
print("Total anomalies : ", target.sum())
print("Detected anomalies : ", predictions.sum())
print("Correct anomalies : ", (predictions*target).sum())
print("Missed anomalies : ", ((1-predictions)*target).sum())
print(f'Precision: {precision:.2f}, Recall: {recall:.2f}, F1: {(2*precision*recall)/(precision + recall):.2f}')

from sklearn.metrics import confusion_matrix
import seaborn as sns
CM = confusion_matrix(target,predictions)
# Assuming CM is your confusion matrix
print("Confusion Matrix = \n", CM, "\n")

# Set up the matplotlib figure
plt.figure(figsize=(8, 6))

# Create the heatmap
sns.heatmap(CM, annot=True, fmt='d', center=0, cmap='Reds', cbar=True)

# Add labels and title
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix Heatmap')

# Show the plot
plt.show()