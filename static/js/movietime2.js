/*eslint-env jquery*/
//    MovieGo
//    Copyright (C) 2017  Charlie J Smotherman
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see <https://www.gnu.org/licenses/>.

function makeGrid1(aimglist) {
	var bb1 = "<div class='oddone ui-body ui-body-b'>"
	var blkAImg1 = "<a href='#intro'><img id='" + aimglist.MediaId + "' class='blkAImg' src='" + aimglist.Artwork + "'></img></a>";
	var closeA1 = "</div>";
	var mg1 = bb1 + blkAImg1 + closeA1;
	return mg1;
}

/*
function makeGrid2(aimglist) {
	var grid = "<div class='ui-grid-a'>";
	var blkA = "<div class='ui-block-a'>";
	var barA = "<div class='ui-bar ui-bar-b'>";
	var blkAImg = "<a href='#intro'><img id='" + aimglist[0].MediaId + "' class='blkAImg' src='" + aimglist[0].Artwork + "'></img>";
	var closeA = "</div></div>";
	var blkB = "<div class='ui-block-b'>";
	var barB = "<div class='ui-bar ui-bar-b'>";
	var blkBImg = "<a href='#intro'><img id='" + aimglist[1].MediaId + "' class='blkBImg' src='" + aimglist[1].Artwork + "'></img></a>";
	var closeB = "</div></div>";
	var closeGrid = "</div>";
	var nblk2 = grid + blkA + barA + blkAImg + closeA + blkB + barB + blkBImg + closeB + closeGrid;
	return nblk2;
};*/

var initMtime = function () {
	$("#foo3, #foo4, #doneBtn, #update2").hide();
};
$(window).load(initMtime)

$(document).on('click', '#movimg', function () {
	$('#foo3').toggle();
})
.on('click', '#tvimg', function () {
	$('#foo4').toggle();
})
.on('click', '.blkAImg, .blkBImg, .blkCImg, .blkDImg', function () {
	var movid = $(this).attr('id');
	$.get("PlayMedia",
	{
		"mid": movid
	},
	function(data) {
		return data;
	})
})
.on('click', '#sttv1', function () {
	$('#sttvMain').empty();
	$.get('STTVs1', function (data) {
		var sttv1e1 = "<ul id='sttvs1' data-role='list-view'>";
		var sttv1f1 = '';
		$.each(data.STTVS1, function ( sttv1key, sttv1val ) {
			var sttv1e2 = "<li><a href='#intro' class='sttvBtn' id='" + sttv1val.MediaId;
			var sttv1e3 = "'><span class='ui-li-count'>" + sttv1val.Episode + "</span>" + sttv1val.Title + "</a></li>";
			sttv1f1 = sttv1f1 + sttv1e2 + sttv1e3;
			return sttv1f1;
		})
		var sttv1foo = sttv1e1 + sttv1f1;
		$('#sttvMain').append(sttv1foo);
		$('#sttvs1').listview().trigger('refresh');
	})
})
.on('click', '#sttv2', function () {
	$('#sttvMain').empty();
	$.get('STTVs2', function (data) {
		var sttv2e1 = "<ul id='sttvs2' data-role='list-view'>";
		var sttv2f1 = '';
		$.each(data.STTVS2, function ( sttv2key, sttv2val ) {
			var sttv2e2 = "<li><a href='#intro' class='sttv2Btn' id='" + sttv2val.MediaId;
			var sttv2e3 = "'><span class='ui-li-count'>" + sttv2val.Episode + "</span>" + sttv2val.Title + "</a></li>";
			sttv2f1 = sttv2f1 + sttv2e2 + sttv2e3;
			return sttv2f1;
		})
		var sttv2foo = sttv2e1 + sttv2f1;
		$('#sttvMain').append(sttv2foo);
		$('#sttvs2').listview().trigger('refresh');
	})
})
.on('click', '#sttv3', function () {
	$('#sttvMain').empty();
	$.get('STTVs3', function (data) {
		var sttv3e1 = "<ul id='sttvs3' data-role='list-view'>";
		var sttv3f1 = '';
		$.each(data.STTVS3, function ( sttv3key, sttv3val ) {
			var sttv3e2 = "<li><a href='#intro' class='sttv3Btn' id='" + sttv3val.MediaId;
			var sttv3e3 = "'><span class='ui-li-count'>" + sttv3val.Episode + "</span>" + sttv3val.Title + "</a></li>";
			sttv3f1 = sttv3f1 + sttv3e2 + sttv3e3;
			return sttv3f1;
		})
		var sttv3foo = sttv3e1 + sttv3f1;
		$('#sttvMain').append(sttv3foo);
		$('#sttvs3').listview().trigger('refresh');
	})
})
.on('click', '.sttvBtn, .sttv2Btn, .sttv3Btn', function () {
	var sttvepisodeid = $(this).attr('id');
	$.get("PlayMedia",
	{
		"mid": sttvepisodeid
	},
	function(data) {
		return data;
	})
})
.on('click', '#tng1', function () {
	$('#tngMain').empty();
	$.get('TNGs1', function (data) {
		var tng1e1 = "<ul id='tngs1' data-role='list-view'>";
		var tng1f1 = '';
		$.each(data.TNGS1, function ( tng1key, tng1val ) {
			var tng1e2 = "<li><a href='#intro' class='tng1Btn' id='" + tng1val.MediaId;
			var tng1e3 = "'><span class='ui-li-count'>" + tng1val.Episode + "</span>" + tng1val.Title + "</a></li>";
			tng1f1 = tng1f1 + tng1e2 + tng1e3;
			return tng1f1;
		})
		var tng1foo = tng1e1 + tng1f1;
		$('#tngMain').append(tng1foo);
		$('#tngs1').listview().trigger('refresh');
	})
})
.on('click', '#tng2', function () {
	$('#tngMain').empty();
	$.get('TNGs2', function (data) {
		var tng2e1 = "<ul id='tngs2' data-role='list-view'>";
		var tng2f1 = '';
		$.each(data.TNGS2, function ( tng2key, tng2val ) {
			var tng2e2 = "<li><a href='#intro' class='tng2Btn' id='" + tng2val.MediaId;
			var tng2e3 = "'><span class='ui-li-count'>" + tng2val.Episode + "</span>" + tng2val.Title + "</a></li>";
			tng2f1 = tng2f1 + tng2e2 + tng2e3;
			return tng2f1;
		})
		var tng2foo = tng2e1 + tng2f1;
		$('#tngMain').append(tng2foo);
		$('#tngs2').listview().trigger('refresh');
	})
})
.on('click', '#tng3', function () {
	$('#tngMain').empty();
	$.get('TNGs3', function (data) {
		var tng3e1 = "<ul id='tngs3' data-role='list-view'>";
		var tng3f1 = '';
		$.each(data.TNGS3, function ( tng3key, tng3val ) {
			var tng3e2 = "<li><a href='#intro' class='tng3Btn' id='" + tng3val.MediaId;
			var tng3e3 = "'><span class='ui-li-count'>" + tng3val.Episode + "</span>" + tng3val.Title + "</a></li>";
			tng3f1 = tng3f1 + tng3e2 + tng3e3;
			return tng3f1;
		})
		var tng3foo = tng3e1 + tng3f1;
		$('#tngMain').append(tng3foo);
		$('#tngs3').listview().trigger('refresh');
	})
})
.on('click', '#tng4', function () {
	$('#tngMain').empty();
	$.get('TNGs4', function (data) {
		var tng4e1 = "<ul id='tngs4' data-role='list-view'>";
		var tng4f1 = '';
		$.each(data.TNGS4, function ( tng4key, tng4val ) {
			var tng4e2 = "<li><a href='#intro' class='tng4Btn' id='" + tng4val.MediaId;
			var tng4e3 = "'><span class='ui-li-count'>" + tng4val.Episode + "</span>" + tng4val.Title + "</a></li>";
			tng4f1 = tng4f1 + tng4e2 + tng4e3;
			return tng4f1;
		})
		var tng4foo = tng4e1 + tng4f1;
		$('#tngMain').append(tng4foo);
		$('#tngs4').listview().trigger('refresh');
	})
})
.on('click', '#tng5', function () {
	$('#tngMain').empty();
	$.get('TNGs5', function (data) {
		var tng5e1 = "<ul id='tngs5' data-role='list-view'>";
		var tng5f1 = '';
		$.each(data.TNGS5, function ( tng5key, tng5val ) {
			var tng5e2 = "<li><a href='#intro' class='tng5Btn' id='" + tng5val.MediaId;
			var tng5e3 = "'><span class='ui-li-count'>" + tng5val.Episode + "</span>" + tng5val.Title + "</li>";
			var tng5f2 = tng5f1 + tng5e2 + tng5e3;
			return tng5f2;
		})
		var tng5foo = tng5e1 + tng5f1;
		$('#tngMain').append(tng5foo);
		$('#tngs5').listview().trigger('refresh');
	})
})
.on('click', '#tng6', function () {
	$('#tngMain').empty();
	$.get('TNGs6', function (data) {
		var tng6e1 = "<ul id='tngs6' data-role='list-view'>";
		var tng6f1 = '';
		$.each(data.TNGS6, function ( tng6key, tng6val ) {
			var tng6e2 = "<li><a href='#intro' class='tng6Btn' id='" + tng6val.MediaId;
			var tng6e3 = "'><span class='ui-li-count'>" + tng6val.Episode + "</span>" + tng6val.Title + "</a></li>";
			tng6f1 = tng6f1 + tng6e2 + tng6e3;
			return tng6f1;
		})
		var tng6foo = tng6e1 + tng6f1;
		$('#tngMain').append(tng6foo);
		$('#tngs6').listview().trigger('refresh');
	})
})
.on('click', '#tng7', function () {
	$('#tngMain').empty();
	$.get('TNGs7', function (data) {
		var tng7e1 = "<ul id='tngs7' data-role='list-view'>";
		var tng7f1 = '';
		$.each(data.TNGS7, function ( tng7key, tng7val ) {
			var tng7e2 = "<li><a href='#intro' class='tng7Btn' id='" + tng7val.MediaId;
			var tng7e3 = "'><span class='ui-li-count'>" + tng7val.Episode + "</span>" + tng7val.Title + "</a></li>";
			tng7f1 = tng7f1 + tng7e2 + tng7e3;
			return tng7f1;
		})
		var tng7foo = tng7e1 + tng7f1;
		$('#tngMain').append(tng7foo);
		$('#tngs7').listview().trigger('refresh');
	})
})
.on('click', '.tng1Btn, .tng2Btn, .tng3Btn, .tng4Btn, .tng5Btn, .tng6Btn, .tng7Btn', function () {
	var tngepisodeid1 = $(this).attr('id');
	$.get("PlayMedia",
	{
		"mid": tngepisodeid1
	},
	function(data) {
		console.log(tngepisodeid1);
	})
})
.on('click', '#voy1', function () {
	$('#voyMain').empty();
	$.get('VOYs1', function (data) {
		var voy1e1 = "<ul id='voys1' data-role='list-view'>";
		var voy1f1 = '';
		$.each(data.VOYS1, function ( voy1key, voy1val ) {
			var voy1e2 = "<li><a href='#intro' class='voy1Btn' id='" + voy1val.MediaId;
			var voy1e3 = "'><span class='ui-li-count'>" + voy1val.Episode + "</span>" + voy1val.Title + "</a></li>";
			voy1f1 = voy1f1 + voy1e2 + voy1e3;
			return voy1f1;
		})
		var voy1foo = voy1e1 + voy1f1;
		$('#voyMain').append(voy1foo);
		$('#voys1').listview().trigger('refresh');
	})
})
.on('click', '#voy2', function () {
	$('#voyMain').empty();
	$.get('VOYs2', function (data) {
		var voy2e1 = "<ul id='voys2' data-role='list-view'>";
		var voy2f1 = '';
		$.each(data.VOYS2, function ( voy2key, voy2val ) {
			var voy2e2 = "<li class='voy2Btn' id='" + voy2val.MediaId;
			var voy2e3 = "'><span class='ui-li-count'>" + voy2val.Episode + "</span>" + voy2val.Title + "</li>";
			voy2f1 = voy2f1 + voy2e2 + voy2e3;
			return voy2f1;
		})
		var voy2foo = voy2e1 + voy2f1;
		$('#voyMain').append(voy2foo);
		$('#voys2').listview().trigger('refresh');
	})
})
.on('click', '#voy3', function () {
	$('#voyMain').empty();
	$.get('VOYs3', function (data) {
		var voy3e1 = "<ul id='voys3' data-role='list-view'>";
		var voy3f1 = '';
		$.each(data.VOYS3, function ( voy3key, voy3val ) {
			var voy3e2 = "<li><a href='#intro' class='voy3Btn' id='" + voy3val.MediaId;
			var voy3e3 = "'><span class='ui-li-count'>" + voy3val.Episode + "</span>" + voy3val.Title + "</a></li>";
			voy3f1 = voy3f1 + voy3e2 + voy3e3;
			return voy3f1;
		})
		var voy3foo = voy3e1 + voy3f1;
		$('#voyMain').append(voy3foo);
		$('#voys3').listview().trigger('refresh');
	})
})
.on('click', '#voy4', function () {
	$('#voyMain').empty();
	$.get('VOYs4', function (data) {
		var voy4e1 = "<ul id='voys4' data-role='list-view'>";
		var voy4f1 = '';
		$.each(data.VOYS4, function ( voy4key, voy4val ) {
			var voy4e2 = "<li><a href='#intro' class='voy4Btn' id='" + voy4val.MediaId;
			var voy4e3 = "'><span class='ui-li-count'>" + voy4val.Episode + "</span>" + voy4val.Title + "</a></li>";
			voy4f1 = voy4f1 + voy4e2 + voy4e3;
			return voy4f1;
		})
		var voy4foo = voy4e1 + voy4f1;
		$('#voyMain').append(voy4foo);
		$('#voys4').listview().trigger('refresh');
	})
})
.on('click', '#voy5', function () {
	$('#voyMain').empty();
	$.get('VOYs5', function (data) {
		var voy5e1 = "<ul id='voys5' data-role='list-view'>";
		var voy5f1 = '';
		$.each(data.VOYS5, function ( voy5key, voy5val ) {
			var voy5e2 = "<li><a href='#intro' class='voy5Btn' id='" + voy5val.MediaId;
			var voy5e3 = "'><span class='ui-li-count'>" + voy5val.Episode + "</span>" + voy5val.Title + "</a></li>";
			voy5f1 = voy5f1 + voy5e2 + voy5e3;
			return voy5f1;
		})
		var voy5foo = voy5e1 + voy5f1;
		$('#voyMain').append(voy5foo);
		$('#voys5').listview().trigger('refresh');
	})
})
.on('click', '#voy6', function () {
	$('#voyMain').empty();
	$.get('VOYs6', function (data) {
		var voy6e1 = "<ul id='voys6' data-role='list-view'>";
		var voy6f1 = '';
		$.each(data.VOYS6, function ( voy6key, voy6val ) {
			var voy6e2 = "<li><a href='#intro' class='voy6Btn' id='" + voy6val.MediaId;
			var voy6e3 = "'><span class='ui-li-count'>" + voy6val.Episode + "</span>" + voy6val.Title + "</a></li>";
			voy6f1 = voy6f1 + voy6e2 + voy6e3;
			return voy6f1;
		})
		var voy6foo = voy6e1 + voy6f1;
		$('#voyMain').append(voy6foo);
		$('#voys6').listview().trigger('refresh');
	})
})
.on('click', '#voy7', function () {
	$('#voyMain').empty();
	$.get('VOYs7', function (data) {
		var voy7e1 = "<ul id='voys7' data-role='list-view'>";
		var voy7f1 = '';
		$.each(data.VOYS7, function ( voy7key, voy7val ) {
			var voy7e2 = "<li><a href='#intro' class='voy7Btn' id='" + voy7val.MediaId;
			var voy7e3 = "'><span class='ui-li-count'>" + voy7val.Episode + "</span>" + voy7val.Title + "</a></li>";
			voy7f1 = voy7f1 + voy7e2 + voy7e3;
			return voy7f1;
		})
		var voy7foo = voy7e1 + voy7f1;
		$('#voyMain').append(voy7foo);
		$('#voys7').listview().trigger('refresh');
	})
})
.on('click', '.voy1Btn, .voy2Btn, .voy3Btn, .voy4Btn, .voy5Btn, .voy6Btn, .voy7Btn', function () {
	var voyepisodeid1 = $(this).attr('id');
	$.get("PlayMedia",
	{
		"mid": voyepisodeid1
	},
	function(data) {
		return data;
	})
})
.on('click', '#ent1', function () {
	$('#entMain').empty();
	$.get('ENTs1', function (data) {
		var ent1e1 = "<ul id='ents1' data-role='list-view'>";
		var ent1f1 = '';
		$.each(data.ENTS1, function ( ent1key, ent1val ) {
			var ent1e2 = "<li><a href='#intro' class='ent1Btn' id='" + ent1val.MediaId;
			var ent1e3 = "'><span class='ui-li-count'>" + ent1val.Episode + "</span>"+ ent1val.Title + "</a></li>";
			ent1f1 = ent1f1 + ent1e2 + ent1e3;
			return ent1f1;
		})
		var ent1foo = ent1e1 + ent1f1;
		$('#entMain').append(ent1foo);
		$('#ents1').listview().trigger('refresh');
	})
})
.on('click', '#ent2', function () {
	$('#entMain').empty();
	$.get('ENTs2', function (data) {
		var ent2e1 = "<ul id='ents2' data-role='list-view'>";
		var ent2f1 = '';
		$.each(data.ENTS2, function ( ent2key, ent2val ) {
			var ent2e2 = "<li><a href='#intro' class='ent2Btn' id='" + ent2val.MediaId;
			var ent2e3 = "'><span class='ui-li-count'>" + ent2val.Episode + "</span>" + ent2val.Title + "</a></li>";
			var ent2f2 = ent2f1 + ent2e2 + ent2e3;
			return ent2f2;
		})
		var ent2foo = ent2e1 + ent2f1;
		$('#entMain').append(ent2foo);
		$('#ents2').listview().trigger('refresh');
	})
})
.on('click', '#ent3', function () {
	$('#entMain').empty();
	$.get('ENTs3', function (data) {
		var ent3e1 = "<ul id='ents3' data-role='list-view'>";
		var ent3f1 = '';
		$.each(data.ENTS3, function ( ent3key, ent3val ) {
			var ent3e2 = "<li><a href='#intro' class='ent3Btn' id='" + ent3val.MediaId;
			var ent3e3 = "'><span class='ui-li-count'>" + ent3val.Episode + "</span>" + ent3val.Title + "</a></li>";
			ent3f1 = ent3f1 + ent3e2 + ent3e3;
			return ent3f1;
		})
		var ent3foo = ent3e1 + ent3f1;
		$('#entMain').append(ent3foo);
		$('#ents3').listview().trigger('refresh');
	})
})
.on('click', '#ent4', function () {
	$('#entMain').empty();
	$.get('ENTs4', function (data) {
		var ent4e1 = "<ul id='ents4' data-role='list-view'>";
		var ent4f1 = '';
		$.each(data.ENTS4, function ( ent4key, ent4val ) {
			var ent4e2 = "<li><a href='#intro' class='ent4Btn' id='" + ent4val.MediaId;
			var ent4e3 = "'><span class='ui-li-count'>" + ent4val.Episode + "</span>" + ent4val.Title + "</a></li>";
			ent4f1 = ent4f1 + ent4e2 + ent4e3;
			return ent4f1;
		})
		var ent4foo = ent4e1 + ent4f1;
		$('#entMain').append(ent4foo);
		$('#ents4').listview().trigger('refresh');
	})
})
.on('click', '.ent1Btn, .ent2Btn, .ent3Btn, .ent4Btn', function () {
	var entepisodeid1 = $(this).attr('id');
	$.get("PlayMedia",
	{
		"mid": entepisodeid1
	},
	function(data) {
		return data;
	})
})
.on('click', '#dis1', function () {
	$('#disMain').empty();
	$.get('DISs1', function (data) {
		var dis1e1 = "<ul id='diss1' data-role='list-view'>";
		var dis1f1 = '';
		$.each(data.DISS1, function ( dis1key, dis1val ) {
			var dis1e2 = "<li><a href='#intro' class='dis1Btn' id='" + dis1val.MediaId;
			var dis1e3 = "'><span class='ui-li-count'>" + dis1val.Episode + "</span>" + dis1val.Title + "</a></li>";
			dis1f1 = dis1f1 + dis1e2 + dis1e3;
			return dis1f1;
		})
		var dis1foo = dis1e1 + dis1f1;
		$('#disMain').append(dis1foo);
		$('#diss1').listview().trigger('refresh');
	})
})
.on('click', '.dis1Btn', function () {
	var disepisodeid1 = $(this).attr('id');
	$.get("PlayMedia",
	{
		"mid": disepisodeid1
	},
	function(data) {
		return data;
	})
})
.on('click', '#orv1', function () {
	$('#orvMain').empty();
	$.get('ORVs1', function (data) {
		var orv1e1 = "<ul id='orvs1' data-role='list-view'>";
		var orv1f1 = '';
		$.each(data.ORVS1, function ( orv1key, orv1val ) {
			var orv1e2 = "<li><a href='#intro' class='orvs1Btn' id='" + orv1val.MediaId;
			var orv1e3 = "'><span class='ui-li-count'>" + orv1val.Episode + "</span>" + orv1val.Title + "</a></li>";
			orv1f1 = orv1f1 + orv1e2 + orv1e3;
			return orv1f1;
		})
		var orv1foo = orv1e1 + orv1f1;
		$('#orvMain').append(orv1foo);
		$('#orvs1').listview().trigger('refresh');
	})
})
.on('click', '.orvs1Btn', function () {
	var orvepisodeid1 = $(this).attr('id');
	$.get("PlayMedia",
	{
		"mid": orvepisodeid1
	},
	function(data) {
		return data;
	})
})
.on('click', '#tls1', function () {
	$('#tlsMain').empty();
	$.get('TLSs1', function (data) {
		var tls1e1 = "<ul id='tlss1' data-role='list-view'>";
		var tls1f1 = '';
		$.each(data.TLSS1, function ( tls1key, tls1val ) {
			var tls1e2 = "<li><a href='#intro' class='tlss1Btn' id='" + tls1val.MediaId;
			var tls1e3 = "'><span class='ui-li-count'>" + tls1val.Episode + "</span>" + tls1val.Title + "</a></li>";
			tls1f1 = tls1f1 + tls1e2 + tls1e3;
			return tls1f1;
		})
		var tls1foo = tls1e1 + tls1f1;
		$('#tlsMain').append(tls1foo);
		$('#tlss1').listview().trigger('refresh');
	})
})
.on('click', '.tlss1Btn', function () {
	var tlsepisodeid1 = $(this).attr('id');
	$.get("PlayMedia",
	{
		"mid": tlsepisodeid1
	},
	function(data) {
		return data;
	})
})
.on('click', '#tls2', function () {
	$('#tlsMain').empty();
	$.get('TLSs2', function (data) {
		var tls2e1 = "<ul id='tlss2' data-role='list-view'>";
		var tls2f1 = '';
		$.each(data.TLSS2, function ( tls2key, tls2val ) {
			var tls2e2 = "<li><a href='#intro' class='tlss2Btn' id='" + tls2val.MediaId;
			var tls2e3 = "'><span class='ui-li-count'>" + tls2val.Episode + "</span>" + tls2val.Title + "</a></li>";
			tls2f1 = tls2f1 + tls2e2 + tls2e3;
			return tls2f1;
		})
		var tls2foo = tls2e1 + tls2f1;
		$('#tlsMain').append(tls2foo);
		$('#tlss2').listview().trigger('refresh');
	})
})
.on('click', '.tlss2Btn', function () {
	var tlsepisodeid2 = $(this).attr('id');
	$.get("PlayMedia",
	{
		"mid": tlsepisodeid2
	},
	function(data) {
		return data;
	})
})
.on('click', '#tls3', function () {
	$('#tlsMain').empty();
	$.get('TLSs3', function (data) {
		var tls3e1 = "<ul id='tlss3' data-role='list-view'>";
		var tls3f1 = '';
		$.each(data.TLSS3, function ( tls3key, tls3val ) {
			var tls3e2 = "<li><a href='#intro' class='tlss3Btn' id='" + tls3val.MediaId;
			var tls3e3 = "'><span class='ui-li-count'>" + tls3val.Episode + "</span>" + tls3val.Title + "</a></li>";
			tls3f1 = tls3f1 + tls3e2 + tls3e3;
			return tls3f1;
		})
		var tls3foo = tls3e1 + tls3f1;
		$('#tlsMain').append(tls3foo);
		$('#tlss3').listview().trigger('refresh');
	})
})
.on('click', '.tlss3Btn', function () {
	var tlsepisodeid3 = $(this).attr('id');
	$.get("PlayMedia",
	{
		"mid": tlsepisodeid3
	},
	function(data) {
		return data;
	})
})
.on('click', '#tls4', function () {
	$('#tlsMain').empty();
	$.get('TLSs4', function (data) {
		var tls4e1 = "<ul id='tlss4' data-role='list-view'>";
		var tls4f1 = '';
		$.each(data.TLSS4, function ( tls4key, tls4val ) {
			var tls4e2 = "<li><a href='#intro' class='tlss4Btn' id='" + tls4val.MediaId;
			var tls4e3 = "'><span class='ui-li-count'>" + tls4val.Episode + "</span>" + tls4val.Title + "</a></li>";
			tls4f1 = tls4f1 + tls4e2 + tls4e3;
			return tls4f1;
		})
		var tls4foo = tls4e1 + tls4f1;
		$('#tlsMain').append(tls4foo);
		$('#tlss4').listview().trigger('refresh');
	})
})
.on('click', '.tlss4Btn', function () {
	var tlsepisodeid4 = $(this).attr('id');
	$.get("PlayMedia",
	{
		"mid": tlsepisodeid4
	},
	function(data) {
		return data;
	})
})
.on('click', '#playBtn', function () {
	$.get('Play', function () {
		//console.log("PlayBtn has been pressed");
	})
})
.on('click', '#pauseBtn', function () {
	$.get('Pause', function () {
		//console.log("PauseBtn has been pressed");
	})
})
.on('click', '#stopBtn', function () {
	$.get('Stop', function () {
		//console.log("StopBtn has been pressed");
	})
})
.on('click', '#nextBtn', function () {
	$.get('Next', function () {
		//console.log("NextBtn has been pressed");
	})
})
.on('click', '#prevBtn', function () {
	$.get('Previous', function () {
		//console.log("PreviousBtn has been pressed");
	})
})
.on('click', '#updateBtn', function () {
	$("#update1").show();
	$("#update2").hide();
	//$('#updateStart').html("Updating Video Library").delay('fast').fadeIn();
	$.get('Update', function (data) {
		if (data.EX.exit != 1) {
			$("#update1").hide()
			$("#update2, #doneBtn").show()
			
		}
	})
.on('click', 'shutdownBtn', function () {
	$.get('ShutDown', function () {
		//console.log("Shutting Down")	
	})
})
.on('click', ".show-page-loading-msg", function () {
	var $this = $(this),
		theme = $this.jqmData("theme") ||
$.mobile.loader.prototype.options.theme,
		msgText = $this.jqmData('msgtext') ||
$.mobile.loader.prototype.options.text,
		textVisible = $this.jqmData("textvisible") ||
$.mobile.loader.prototype.options.textVisible,
		textonly = !!$this.jqmData('textonly');
		var html1 = $this.jqmData("html") || "";
	$.mobile.loading("show", {
			text: msgText,
			textVisible: textVisible,
			theme: theme,
			textonly: textonly,
			html: html1,
	});
})
.on('click', "#actionBtn", function () {
	if ($('#actionMain').children().length === 0){
		$.get('IntAction', function (data) {
			$.each(data.IntAction, function ( Actionkey, Actionval ) {
				var Actionarr1 = makeGrid1(Actionval);
				$('#actionMain').append(Actionarr1);
			})
		})
	}
})
.on('click', '#cartoonsBtn', function () {
	if ($('#cartoonsMain').children().length === 0){
		$.get('IntCartoons', function (data) {
			$.each(data.IntCartoons, function ( Cartoonskey, Cartoonsval ) {
				var Cartoonsarr3 = makeGrid1(Cartoonsval);
				$('#cartoonsMain').append(Cartoonsarr3);
			})
		})
	}
})
.on('click', '#comedyBtn', function () {
	if ($('#comedyMain').children().length === 0){
		$.get('IntComedy', function (data) {
			$.each(data.IntComedy, function ( Comedykey, Comedyval ) {
				var Comedyarr1 = makeGrid1(Comedyval);
				$('#comedyMain').append(Comedyarr1);
			})
		})
	}
})
.on('click', '#dramaBtn', function () {
	if ($('#dramaMain').children().length === 0){
		$.get('IntDrama', function (data) {
			$.each(data.IntDrama, function ( Dramakey, Dramaval ) {
				var Dramaarr3 = makeGrid1(Dramaval);
				$('#dramaMain').append(Dramaarr3);
			})
		})
	}
})
.on('click', '#godzillaBtn', function () {
	if ($('#godzillaMain').children().length === 0){
		$.get('IntGodzilla', function (data) {
			$.each(data.IntGodzilla, function ( GodzillaKey, GodzillaVal) {
				var Godzillaarr1 = makeGrid1(GodzillaVal);
				$('#godzillaMain').append(Godzillaarr1);
			})
		})
	}
})
.on('click', '#harrypotterBtn', function () {
	if ($('#harrypotterMain').children().length === 0){
		$.get('IntHarryPotter', function (data) {
			$.each(data.IntHarryPotter, function ( HPkey, HPval ) {
				var HParr1 = makeGrid1(HPval);
				$('#harrypotterMain').append(HParr1);
			})
		})
	}
})
.on('click', '#indianajonesBtn', function () {
	if ($('#indianajonesMain').children().length === 0){
		$.get('IntIndianaJones', function (data) {
			$.each(data.IntIndianaJones, function ( ijkey, ijval ) {
				var IndianaJonesarr1 = makeGrid1(ijval);
				$('#indianajonesMain').append(IndianaJonesarr1);
			})
		})
	}
})
.on("click", "#johnwayneBtn", function () {
	if ($('#johnwayneMain').children().length === 0){
		$.get('IntJohnWayne', function (data) {
			$.each(data.IntJohnWayne, function ( JohnWaynekey, JohnWayneval ) {
				var JohnWaynearr1 = makeGrid1(JohnWayneval);
				$('#johnwayneMain').append(JohnWaynearr1);
			})
		})
	}
})
.on("click", "#jurassicparkBtn", function () {
	if ($('#jurassicparkMain').children().length === 0){
		$.get('IntJurassicPark', function (data) {
			$.each(data.IntJurasicPark, function (jurkey, jurval) {
				var JParr1 = makeGrid1(jurval);
				$('#jurassicparkMain').append(JParr1);
			})
		})
	}
})
.on('click', '#kingsmanBtn', function () {
	if ($('#kingsmanMain').children().length === 0){
		$.get('IntKingsMan', function (data) {
			$.each(data.IntKingsMan, function ( Kingkey, Kingval ) {
				var Kingsmanarr2 = makeGrid1(Kingval);
				$('#kingsmanMain').append(Kingsmanarr2);
			})
		})
	}
})
.on('click', '#meninblackBtn', function () {
	if ($('#meninblackMain').children().length === 0){
		$.get('IntMenInBlack', function (data) {
			$.each(data.IntMenInBlack, function (mibkey, mibval) {
				var MIBarr1 = makeGrid1(mibval);
				$('#meninblackMain').append(MIBarr1);	
			})
		})
	}
})
.on('click', '#scifiBtn', function () {
	if ($('#scifiMain').children().length === 0){
		$.get('IntSciFi', function (data) {
			$.each(data.IntSciFi, function ( SciFikey, SciFival ) {
				var SciFiarr1 = makeGrid1(SciFival);
				$('#scifiMain').append(SciFiarr1);
			})
		})
	}
})
.on('click', '#starwarsBtn', function () {
	if ($('#starwarsMain').children().length === 0){
		$.get('IntStarWars', function (data) {
			$.each(data.IntStarWars, function ( key, val ) {
				var arr1 = makeGrid1(val);
				$('#starwarsMain').append(arr1);
			})
		})
	}
})
.on('click', '#startrekMBtn', function () {
	if ($('#startrekMain').children().length === 0){
		$.get('IntStarTrek', function (data) {
			$.each(data.IntStarTrek, function ( StarTrekkey, StarTrekval ) {
				var StarTrekarr1 = makeGrid1(StarTrekval);
				$('#startrekMain').append(StarTrekarr1);
			})
		})
	}
})
.on('click', '#superherosBtn', function () {
	if ($('#superherosMain').children().length === 0){
		$.get('IntSuperHeros', function (data) {
			$.each(data.IntSuperHeros, function ( shkey, shval ) {
				var sharr1 = makeGrid1(shval);
				$('#superherosMain').append(sharr1);
			})
		})
	}
})
.on('click', '#tremorsBtn', function () {
	if ($('#tremorsMain').children().length === 0){
		$.get('IntTremors', function (data) {
			$.each(data.IntTremors, function (Tremorskey, Tremorsval) {
				var HParr1 = makeGrid1(Tremorsval);
				$('#tremorsMain').append(HParr1);
			})
		})
	}
})
.on('click', '#miscBtn', function () {
	if ($('#miscMain').children().length === 0){
		$.get('IntMisc', function (data) {
			$.each(data.IntMisc, function ( Misckey, Miscval ) {
				var Miscarr1 = makeGrid1(Miscval);
				$('#miscMain').append(Miscarr1);
			})
		})
	}
})
})