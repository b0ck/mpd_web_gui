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
    songNode.find('button.add').attr('file', song.file);
    songNode.find('button.play').attr('file', song.file);
    songNode.find('span.badge-secondary').text(song.track);
    songNode.find('span.title').text(song.title);
    songNode.find('span.badge-primary').text(makeLengthReadable(song.length));
    return songNode;
}

function buildSongCurrent(song) {
    const songNode = $('#templates.hidden .song-current').clone(true);
    songNode.find('button.delete-current').attr('pos', song.pos);
    songNode.find('button.play-current').attr('pos', song.pos);
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

function playPos(pos) {
    socket.emit('command', {'cmd':'play_pos', 'data':{'pos':pos}});
}

function playSong(file) {
    socket.emit('command', {'cmd':'play_song', 'data':{'song':file}});
}

function addSong(file) {
    socket.emit('command', {'cmd':'add_song', 'data':{'song':file}});
}

function deleteSong(pos) {
    socket.emit('command', {'cmd':'delete_song', 'data':{'pos':pos}});
}

function initPlayButtonClickListener() {
    $('.btn.play').click(function() {
        var item = $(this).parent().parent();
        updateSelection(item, '#songs');
        playSong($(this).attr('file'));
    });
    $('.btn.add').click(function() {
        addSong($(this).attr('file'));
    });
    $('.btn.play-current').click(function() {
        playPos($(this).attr('pos'));
    });
    $('.btn.delete-current').click(function() {
        deleteSong($(this).attr('pos'));
    });
}

function initAlbumClickListener() {
    const albums = $('li.album');

    albums.click(function() {
        updateSelection(this, '#albums');

        const requestParams = {
            'artist': $('#artists .active').text(),
            'album': $(this).find('.title').text()
        };

        $('#nav-songs-tab').tab('show');

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
        $('#nav-albums-tab').tab('show');

        updateList(
            '/albums',
            requestParams,
            $('#albums'),
            buildAlbum);
    });
}

$(function(){
    initArtistClickListener();
    initAlbumClickListener();
    initPlayButtonClickListener();
});