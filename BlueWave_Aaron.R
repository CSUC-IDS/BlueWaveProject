library(caret)
library(lubridate)
library(dplyr)
library(e1071)
library(tidyr)
library(tools)
library(magrittr)

CSA <- read.csv('~/math485/BlueWaveProject/data/CandidateSummaryAction.csv', stringsAsFactors = FALSE)
senate <- read.csv("~/math485/BlueWaveProject/senate.csv")
house  <- read.csv("~/math485/BlueWaveProject/house.csv")
senate <- separate(senate,Date, into = c("Weekday","Month","Day"), convert = TRUE, sep = " ")
house <- separate(house,Date, into = c("Weekday","Month","Day"), convert = TRUE, sep = " ")
senate <- separate(senate,Spread, into = c("Victor","Difference"), convert = TRUE, sep = " ")
house <- separate(house,Spread, into = c("Victor","Difference"), convert = TRUE, sep = " ")
senate$Difference[is.na(senate$Difference)] <- 0
house$Difference[is.na(house$Difference)] <- 0

CSA.small <- CSA %>% select(can_nam,can_sta,can_par_aff)
head(CSA.small)
CSA.split <- separate(CSA.small,can_nam,into = c("Results","first_name"),sep=", ")
CSA.split$Results <- toTitleCase(tolower(CSA.split$Results))

head(senate)
head(house)

senate_new <- left_join(senate, CSA.split, by="Results")
house_new <- left_join(house,CSA.split, by="Results")
head(senate_new)
head(house_new)

senate_new$Votes <- as.numeric(senate_new$Votes)
house_new$Votes <- as.numeric(house_new$Votes)

senate_aggvotes <- na.omit(senate) %>% group_by(Weekday, Month, Day,Race,Poll,Victor,Difference) %>% mutate(Total.Votes = sum(Votes)) %>% unique()
house_aggvotes <- na.omit(house) %>% group_by(Weekday, Month, Day,Race,Poll,Victor,Difference) %>% mutate(Total.Votes = sum(Votes)) %>% unique()

senate.final <- na.omit(left_join(senate_new,senate_aggvotes))
house.final <- na.omit(left_join(house_new,house_aggvotes))

senate.final$perVotes <- senate.final$Votes/senate.final$Total.Votes
house.final$perVotes <- house.final$Votes/house.final$Total.Votes

head(senate.final)
head(house.final)

senate.model <- glm(perVotes ~ 0 + Month + Day + can_sta + can_par_aff, data = senate.final)
summary(senate.model)
senatepred.votes <- predict(senate.model,newdata = senate.final)
senate.END <- cbind(senate.final,senatepred.votes)
senate.total.votes <- senate.END %>% group_by(can_par_aff) %>% summarise(mean(senatepred.votes))
names(senate.total.votes) <- c("Party","MeanVotes")
senate.total.votes$MeanVotes * 33



house.model <- glm(perVotes ~ 0 + Month + Day + can_sta + can_par_aff, data = house.final)
summary(house.model)
housepred.votes <- predict(house.model,newdata = house.final)
house.END <- cbind(house.final,housepred.votes)
house.total.votes <- house.END %>% group_by(can_par_aff) %>% summarise(mean(housepred.votes))
names(house.total.votes) <- c("Party","MeanVotes")
house.total.votes$MeanVotes * 435



