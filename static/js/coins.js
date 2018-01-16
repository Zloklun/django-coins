d = document;
processed = false;
media_root = undefined;

data = undefined;
currencies_dict = {},
countries_dict = {},
mints_dict = {},
series_dict = {};


load_data = function(url)
{
    return new Promise(function(resolve, reject)
    {
        // Main code
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.onreadystatechange = function()
        {
            if (xhr.readyState != XMLHttpRequest.DONE)
                return;
            if ((xhr.status < 200) || (xhr.status >= 400))
                return reject(xhr.status + ': ' + xhr.statusText);

            data = JSON.parse(xhr.responseText);
            for (var field in data)
            {
                if (field !== 'title')
                {
                    data[field] = JSON.parse(data[field]);
                    for (var item in data[field])
                        data[field][item] = flatten_object(data[field][item])
                }
            }
            processed = true;
            resolve(data);
        }
        xhr.send();
    });
}


function flatten_object(object)
{
    var result = {};
    result.model = object.model;
    result.pk = object.pk;
    for (var key in object.fields)
        result[key] = object.fields[key];
    return result;
}


function get_currency(pk)
{
    if (pk === null)
        return null;
    if (currencies_dict[pk] === undefined)
    {
        var found = false;
        for (var i = 0; i < data.currencies.length; ++i)
        {
            if (data.currencies[i].pk == pk)
            {
                currencies_dict[pk] = data.currencies[i];
                found = true;
                break;
            }
        }
        if (!found)
            currencies_dict[pk] = { symbol : '★' };
    }
    return currencies_dict[pk];
}


function get_country(pk)
{
    if (pk === null)
        return null;
    if (countries_dict[pk] === undefined)
    {
        var found = false;
        for (var i = 0; i < data.countries.length; ++i)
        {
            if (data.countries[i].pk == pk)
            {
                countries_dict[pk] = data.countries[i];
                found = true;
                break;
            }
        }
        if (!found)
            countries_dict[pk] = null;
    }
    return countries_dict[pk];
}


function get_country_by_code(code)
{
    if (!code)
        return undefined;
    for (var i = 0; i < data.countries.length; ++i)
        if (data.countries[i].code === code)
            return data.countries[i].pk;
}


function get_mint(pk)
{
    if (pk === null)
        return null;
    if (mints_dict[pk] === undefined)
    {
        var found = false;
        for (var i = 0; i < data.mints.length; ++i)
            if (data.mints[i].pk == pk)
            {
                mints_dict[pk] = data.mints[i];
                found = true;
                break;
            }
        if (!found)
            mints_dict[pk] = null;
    }
    return mints_dict[pk];
}


function get_series(pk)
{
    if (pk === null)
        return null;
    if (series_dict[pk] === undefined)
    {
        var found = false;
        for (var i = 0; i < data.series.length; ++i)
            if (data.series[i].pk == pk)
            {
                series_dict[pk] = data.series[i];
                found = true;
                break;
            }
        if (!found)
            series_dict[pk] = null;
    }
    return series_dict[pk];
}



function make_header(index, coin)
{
    var header = d.createElement('h4');

    var counter = d.createElement('small');
    counter.innerHTML = '#' + index + '. ';
    header.appendChild(counter);

    var cur = get_currency(coin.currency);
    var code = (!!cur.symbol) ? cur.symbol : cur.code;

    var title = d.createElement('strong');
    title.title = coin.face_value;
    title.innerHTML = coin.face_value + ' ' + code;
    header.appendChild(title);

    return header;
}


function make_badge(coin)
{
    var badge = d.createElement('span');
    badge.className = 'label label-default';

    country = get_country(coin.country);
    var flag = d.createElement('img');
    flag.className = 'flag';
    flag.title = country.short_name;
    flag.alt = country.code;
    flag.src = media_root + country.flag;
    badge.appendChild(flag);

    badge.innerHTML += ' ' + coin.year;

    mint = get_mint(coin.mint);
    if (mint != null)
        badge.innerHTML += ' ' + mint.tag;

    if (coin.magnetic)
        badge.innerHTML += ' <span class="glyphicon glyphicon-magnet" title="Магнитная"></span>';

    return badge;
}

function make_comment(coin)
{
    if (coin.comment == '')
        return null;

    comment = d.createElement('div');
    comment.className = 'panel-footer';
    comment.innerHTML = '<em>' + coin.comment + '</em>';
    return comment;
}


function make_block(index, coin)
{
    if (coin === undefined)
        return undefined;
    if (coin.model !== 'coins.coin')
        return undefined;

    var container = d.createElement('div');
    container.className = 'col-xs-6 col-md-3 col-lg-2';
    container.style.padding = '2px !important';

    var inner = d.createElement('div');
    inner.className = 'panel panel-info';

    var main_info = d.createElement('div');
    main_info.className = 'panel-body';
    inner.appendChild(main_info);

    main_info.appendChild(make_header(index, coin));
    main_info.appendChild(make_badge(coin));

    var series_block = (function(){
        var series = get_series(coin.series);
        if (series == null)
            return null;

        var block = d.createElement('div')
        block.className = 'panel-body';
        var par = d.createElement('p');
        par.innerHTML = 'Входит в серию <em>«' + series.name + '»</em>';
        if (coin.series_item != null)
            par.innerHTML += ' (' + coin.series_item + ')';
        block.appendChild(par)
        return block;
    })();
    if (series_block != null)
        main_info.appendChild(series_block);

    comment = make_comment(coin);
    if (comment != null)
        inner.appendChild(comment);

    container.appendChild(inner);
    return container;
}


// Fills root element with coins information
function fill_coins(root_element, coin_filter)
{
    if (root_element === undefined)
        return reject('root_element is undefined');
    if (coin_filter === undefined)
        coin_filter = function() { return true; }

    var header = d.createElement('h3');
    header.innerHTML = data.title;
    root_element.appendChild(header);

    var total = data.coins.length;
    var count = 0;
    for (var i = 0; i < total; i++)
    {
        var coin = data.coins[i];
        if (!coin_filter(coin))
            continue;
        try
        {
            block = make_block(count + 1, coin);
            if (block !== undefined)
                root_element.appendChild(block);
            count++;
        } catch (err)
        {
            console.log('Error while displaying coin ' + coin.pk + ': ' +
                        err.name + ' ' + err.message + '\n' + err.stack);
        }
    }
    console.log(count + ' coins displayed, ' + (total - count) + ' are errorneous');
}
