function updateSelection(item, list) {
    $(list).children().removeClass('active');
    $(item).addClass('active');
}

function buildAlbum(album) {
    const albumNode = $('#templates.hidden .album').clone(true);
    albumNode.find('span.badge-secondary').text(album.year);
    albumNode.find('span.title').text(album.title);
    albumNode.find('span.badge-primary').text(makeLengthReadable(album.length));
    return albumNode;
}

function buildSong(song) {
    const songNode = $('#templates.hidden .song').clone(true);
    songNode.find('button').attr('file', song.file);
    songNode.find('span.badge-secondary').text(song.track);
    songNode.find('span.title').text(song.title);
    songNode.find('span.badge-primary').text(makeLengthReadable(song.length));
    return songNode;
}

function updateList(url, params, list, buildNode) {
    $.getJSON(url, params, function(data) {
        list.empty();

        $.each(data, function(key, val) {
            list.append(buildNode(val));
        });
    });
}

function playSong(file) {
    $.get('/play', {'file': file}, function(data){
        refreshSongInformation(data);
        state = 'play';
        switchPlayButton();
    });
}

function initPlayButtonClickListener() {
    $('.btn.play').click(function() {
        var item = $(this).parent().parent();
        updateSelection(item, '#songs');
        playSong($(this).attr('file'));
    })
}

function initAlbumClickListener() {
    const albums = $('li.album');

    albums.click(function() {
        updateSelection(this, '#albums');

        const requestParams = {
            'artist': $('#artists .active').text(),
            'album': $(this).find('.title').text()
        };

        updateList(
            '/songs',
            requestParams,
            $('#songs'),
            buildSong);
    });
}

function initArtistClickListener() {
    const artists = $('#artists');

    artists.children().click(function() {
        updateSelection(this, artists);

        const requestParams = {
            'artist': $(this).text()
        };

        $('#songs').empty();

        updateList(
            '/albums',
            requestParams,
            $('#albums'),
            buildAlbum);
    });
}

$(document).ready(function(){
    initArtistClickListener();
    initAlbumClickListener();
    initPlayButtonClickListener();
});