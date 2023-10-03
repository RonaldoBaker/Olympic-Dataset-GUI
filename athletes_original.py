import sys 
import pandas as pd 
import matplotlib.pyplot as plt

def numberCheck(number): # Checking that the input number is 0 < integer <= 5
    if len(number) > 5: # check that the user hasn't inputted more than 5 options 
        print("Error: Too many options")
        sys.exit()
    #else:
    try:
        tmp = list() # list to store the individual integers
        for i in number:
            if 1 <= int(i) <= 5: # checking they are integers in this range
                tmp.append(i)
            else:
                print("Error: The input must be between 1 - 5")
                sys.exit()
        return tmp
    except(ValueError):
        print("Error: The input must be an integer number. Exiting program.")
        sys.exit()

# function to filter out the dataset in each 'if' condition
# so the dataset is continuously filtered, rather than all the filters being applied at once
def sub_filter(df,filter,option): 
    sub_df = df[(df[filter]==option)]
    return sub_df

# main filtering function to take inputs of which filters to apply to the dataframe
def filter(df):

    sub_df = pd.DataFrame() # creating empty dataframe to assign filtered data to
    # making a copy of the dataframe to be filtered, so that the original data is untouched and can be returned if there are any erros with the chosen filter
    sub_df = df 

    print("Please enter the numbers of the filters you would like to use")
    print("(e.g. 234 if you want to filter by age, team and year):")
    print(" 1.Sex\n 2.Age\n 3.Team\n 4.Year\n 5.Sport")
    filterChoice = numberCheck(input())

    if '1' in filterChoice: # Filter by Sex
        sex = input("Enter F for female, M for male:")
        if sex != 'F' and sex != 'M':
            print("Error: Invalid argument")
            sys.exit()

        sub_df = sub_filter(sub_df,"Sex",sex) # filtering the second dataframe by sex 

    if '2' in filterChoice: # Filter by Age 
        age = input("Enter age in years:")
        try:
            age = int(age)
            if age < 0:
                print("Error: Input must be greater than 0")
                sys.exit()
        except(ValueError):
            print("Error: The input must be exact years and not contain characters")
            sys.exit()
        sub_df = sub_filter(sub_df,"Age",age)

    if '3' in filterChoice: # Filter by Team 
        team = input("Enter the name of the team:")
        valid = any(char.isdigit() for char in team) # checks whether the input includes a digit
        if valid == True: # input includes a digit
            print("Error: Input must not include a number")
            sys.exit()
        sub_df = sub_filter(sub_df,"Team",team)

    if '4' in filterChoice: # Filter by Year 
        year = input("Enter the year:")
        if len(year) > 4: # checking that the year is a valid
            print("Error: Input year is too long")
            sys.exit()
        else:
            try:
                year = int(year)
                if year < 0:
                    print("Error: Input year is invalid")
                    sys.exit()
            except(ValueError):
                print("Error: Input is not an integer")
                sys.exit()
        sub_df = sub_filter(sub_df,"Year",year)  

    if '5' in filterChoice: # Filter by Sport 
        sport = input("Enter the name of sport:")
        valid = any(char.isdigit() for char in sport) # checking if there is a digit in the input
        if valid == True:
            print("Error: Input must not include a number")
            sys.exit()
        sub_df = sub_filter(sub_df,"Sport",sport)


    if (sub_df.empty) == True:
        print("Error: No entries match the chosen filter(s)")
        records = 0
        return df,records  
    else: 
    # if there wasn't an error in filtering the dataframe
    # then the new fully filtered dataframe can be returned with the number of records in that dataframe 
        return sub_df,sub_df.shape[0]

def plot(df,noRecords):
    print("Plotting data...")
    if 0 < noRecords < 100: # creating a scatter graph
        plt.scatter(df['ID'],df['Weight'])
        # labelling axes
        plt.xlabel("ID number"); plt.ylabel("Weight (kg)")
        plt.title("Weight distribution amongst athletes")
        plt.savefig("scatter.png")
        print("-----------------------------------")
        print(f"{noRecords} record(s)")
        print("File scatter.png saved")
        print("-----------------------------------")
    
    elif noRecords >= 100:
        plt.hist(df["Weight"],12)
        # labelling axes
        plt.xlabel("Weight (kg)"); plt.ylabel("Frequency")
        plt.title("Weight distribution amongst athletes")
        plt.savefig("hist.png")
        print("-----------------------------------")
        print(f"{noRecords} record(s)")
        print("File hist.png saved")
        print("-----------------------------------")
    
    elif noRecords == 0:
        print("Error: There is no data in this dataframe to plot")

def main():
    print("Loading dataset...")
    df = pd.read_csv("athlete_events_shortened.csv")
    sub_df,records = filter(df)
    if records == 0:
        print("There were 0 records that matched the chosen filters")
        print("Displaying original data...")
        print(df)
    else:
        print(f"There were {records} record(s) that matched the chosen filters")
        print("Displaying filtered data...")
        print(sub_df)

    noRecords = sub_df.shape[0]
    plot(sub_df,noRecords)

if __name__ == "__main__":
    main()