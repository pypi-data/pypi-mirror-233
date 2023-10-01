def linearsearch(toFind,iterable):
    lengthOfIterable = len(iterable)
    for element in range(lengthOfIterable):
        if toFind==iterable[element]:
            return element+1;
    return None