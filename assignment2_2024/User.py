class User:
    def __init__(self, id, has_labels):
        self.id = id
        self.has_labels = has_labels
        
    def __str__(self):
        return f"{self.id}: {self.has_labels}"
    
    def get_data(self):
        return [self.id, self.has_labels]
    
    
