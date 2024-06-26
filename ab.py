from scipy.stats import shapiro, levene, ttest_ind, mannwhitneyu

class AB:
    def __init__(self, dataframe, group, target):
        self.dataframe = dataframe
        self.group = group
        self.target = target

    def AB_Test(self):    
        # Split A/B
        groupA = self.dataframe[self.dataframe[self.group] == "A"][self.target]
        groupB = self.dataframe[self.dataframe[self.group] == "B"][self.target]
        
        # Assumption: Normality
        ntA = shapiro(groupA)[1] < 0.05
        ntB = shapiro(groupB)[1] < 0.05
        # H0: Distribution is Normal! - False
        # H1: Distribution is not Normal! - True
        
        if (ntA == False) & (ntB == False): # "H0: Normal Distribution"
            # Parametric Test
            # Assumption: Homogeneity of variances
            leveneTest = levene(groupA, groupB)[1] >= 0.05
            test = ttest_ind(groupA, groupB, equal_var=leveneTest)[1]
        else:
            # Non-Parametric Test
            test = mannwhitneyu(groupA, groupB)[1] 
            # H0: M1 == M2 - False
            # H1: M1 != M2 - True
            
        result = {}
        if (ntA == False) & (ntB == False):
            result["Test Type"] = "Parametric"
            if leveneTest:
                result["Homogeneity"] = "Yes"
            else:
                result["Homogeneity"] = "No"
        else:
            result["Test Type"] = "Non-Parametric"
        result["p-value"] = test
        if test < 0.05:
            result["AB Hypothesis"] = "Reject H0"
            result["Comment"] = "A/B groups are not similar!"
        else:
            result["AB Hypothesis"] = "Fail to reject H0"
            result["Comment"] = "A/B groups are similar!"
        
        return result