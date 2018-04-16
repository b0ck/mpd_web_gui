function makeLengthReadable(seconds) {
    const time = new Date(1000 * seconds).toISOString();
    if (seconds < 60)
        return time.substr(17, 2);
    if (seconds < 600)
        return time.substr(15, 4);
    if (seconds < 3600)
        return time.substr(14, 5);
    if (seconds < 36000)
        return time.substr(12, 7);
    return time.substr(11, 8);
}