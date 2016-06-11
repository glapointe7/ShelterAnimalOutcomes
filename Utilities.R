library(lubridate)
library(stringr)
library(xgboost)
library(methods)
library(Matrix)
library(ggplot2)
library(scales)
library(plotrix)
library(dplyr)
library(plyr)
library(MLmetrics)
library(Ckmeans.1d.dp)

## Outcome string constants
Outcome.ADOPTION <- "Adoption"
Outcome.DIED <- "Died"
Outcome.EUTHANASIA <- "Euthanasia"
Outcome.RETURN_TO_OWNER <- "Return_to_owner"
Outcome.TRANSFER <- "Transfer"


CategoryToInteger <- function(feature)
{
    feature.categories <- unique(feature)
    feature.categories.id <- 1:length(feature.categories)
    names(feature.categories.id) <- as.vector(feature.categories)
    feature <- feature.categories.id[feature]
    
    return(feature)
}


GetBooleanFeatureFromGroup <- function(feature, group)
{
    indices <- grep(group, feature)
    feature.is.bool <- rep(0, length(feature))
    feature.is.bool[indices] <- 1
    
    return(feature.is.bool)
}


GetIntegerFeatureFromGroups <- function(feature, groups)
{
    feature.group <- rep(0, length(feature))
    i <- 1
    for(group in groups)
    {
        indices <- grep(group, feature)
        feature.group[indices] <- i
        i <- i + 1
    }
    
    return(feature.group)
}