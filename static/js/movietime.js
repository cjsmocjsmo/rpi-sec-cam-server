/*eslint-env jquery*/
/*
#    MovieGo
#    Copyright (C) 2017  Charlie J Smotherman
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

// function makeGrid1(aimglist) {
// 	var bb1 = "<div class='oddone ui-body ui-body-b'>"
// 	var blkAImg1 = "<a href='#intro'><img id='" + aimglist.MediaId + "' class='blkAImg' src='" + aimglist.Artwork + "'></img></a>";
// 	var closeA1 = "</div>";
// 	var mg1 = bb1 + blkAImg1 + closeA1;
// 	return mg1;
// }
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

/*function makeGrid3(aimglist) {
	var grid = "<div class='ui-grid-b'>";
	var blkA = "<div class='ui-block-a'>";
	var barA = "<div class='ui-bar ui-bar-b'>";
	var blkAImg = "<a href='#intro'><img id='" + aimglist[0].MediaId + "' class='blkAImg' src='" + aimglist[0].HttpArtwork + "'></img></a>";
	var closeA = "</div></div>";
	var blkB = "<div class='ui-block-b'>";
	var barB = "<div class='ui-bar ui-bar-b'>";
	var blkBImg = "<a href='#intro'><img id='" + aimglist[1].MediaId + "' class='blkBImg' src='" + aimglist[1].HttpArtwork + "'></img></a>";
	var closeB = "</div></div>"
	var blkC = "<div class='ui-block-c'>";
	var barC = "<div class='ui-bar ui-bar-b'>";
	var blkCImg = "<a href='#intro'><img id='" + aimglist[2].MediaId + "' class='blkCImg' src='" + aimglist[2].HttpArtwork + "'></img></a>";
	var closeC = "</div></div>";
	var closeGrid = "</div>";
	var n = grid + blkA + barA + blkAImg + closeA;
	var n2 = n + blkB + barB + blkBImg + closeB;
	var n3 = n2 + blkC + barC + blkCImg + closeC + closeGrid;
	return n3;
};*/

// function initSciFi() {
// 	if ($('#scifiMain').children().length === 0){
		
// 		$.get('IntSciFi', function (data) {
// 			$.each(data.IntSciFi, function ( SciFikey, SciFival ) {
// /*			var SciFileng = SciFival.length;
// 			if (SciFileng == 2) {
// 				var SciFiarr2 = makeGrid2(SciFival);
// 				$('#scifiMain').append(SciFiarr2);
// 			}
// 			if (SciFileng == 1) {*/
// 				var SciFiarr1 = makeGrid1(SciFival);
// 				$('#scifiMain').append(SciFiarr1); 			
// 			})
// 		})
// 	}
// }			

// function initAction() {
// 	if ($('#actionMain').children().length === 0){
// 		$.get('IntAction', function (data) {
// 			$.each(data.IntAction, function ( Actionkey, Actionval ) {
// 				var Actionarr1 = makeGrid1(Actionval);
// 				$('#actionMain').append(Actionarr1);
// 			})
// 		})
// 	}
// }

// function initComedy() {
// 	if ($('#comedyMain').children().length === 0){
// 		$.get('IntComedy', function (data) {
// 			$.each(data.IntComedy, function ( Comedykey, Comedyval ) {
// 				var Comedyarr1 = makeGrid1(Comedyval);
// 				$('#comedyMain').append(Comedyarr1);
// 			})
// 		})
// 	}
// }

// function initDrama() {
// 	if ($('#dramaMain').children().length === 0){
// 		$.get('IntDrama', function (data) {
// 			$.each(data.IntDrama, function ( Dramakey, Dramaval ) {
// 				var Dramaarr3 = makeGrid1(Dramaval);
// 				$('#dramaMain').append(Dramaarr3);
// 			})
// 		})
// 	}
// }

// function initCartoons() {
// 	if ($('#cartoonsMain').children().length === 0){
// 		$.get('IntCartoons', function (data) {
// 			$.each(data.IntCartoons, function ( Cartoonskey, Cartoonsval ) {
// 				var Cartoonsarr3 = makeGrid1(Cartoonsval);
// 				$('#cartoonsMain').append(Cartoonsarr3);
// 			})
// 		})
// 	}
// }

// function initKingsman() {
// 	if ($('#kingsmanMain').children().length === 0){
// 		$.get('IntKingsMan', function (data) {
// 			$.each(data.IntKingsMan, function ( Kingkey, Kingval ) {
// 				var Kingsmanarr2 = makeGrid1(Kingval);
// 				$('#kingsmanMain').append(Kingsmanarr2);
// 			})
// 		})
// 	}
// }

// function initGodzilla() {
// 	if ($('#godzillaMain').children().length === 0){
// 		$.get('IntGodzilla', function (data) {
// 			$.each(data.IntGodzilla, function ( GodzillaKey, GodzillaVal) {
// 				var Godzillaarr1 = makeGrid1(GodzillaVal);
// 				$('#godzillaMain').append(Godzillaarr1);
// 			})
// 		})
// 	}
// }

// function initStarTrek() {
// 	if ($('#startrekMain').children().length === 0){
// 		$.get('IntStarTrek', function (data) {
// 			$.each(data.IntStarTrek, function ( StarTrekkey, StarTrekval ) {
// 				var StarTrekarr1 = makeGrid1(StarTrekval);
// 				$('#startrekMain').append(StarTrekarr1);
// 			})
// 		})
// 	}
// }

// function initStarWars() {
// 	if ($('#starwarsMain').children().length === 0){
// 		$.get('IntStarWars', function (data) {
// 			$.each(data.IntStarWars, function ( key, val ) {
// 				var arr1 = makeGrid1(val);
// 				$('#starwarsMain').append(arr1);
// 			})
// 		})
// 	}
// }

/* function initSuperHeros() {
	if ($('#superherosMain').children().length === 0){
		$.get('IntSuperHeros', function (data) {
			$.each(data.IntSuperHeros, function ( shkey, shval ) {
				var sharr1 = makeGrid1(shval);
				$('#superherosMain').append(sharr1);
			})
		})
	}
} */

/* function initIndianaJones() {
	if ($('#indianajonesMain').children().length === 0){
		$.get('IntIndianaJones', function (data) {
			$.each(data.IntIndianaJones, function ( ijkey, ijval ) {
				var IndianaJonesarr1 = makeGrid1(ijval);
				$('#indianajonesMain').append(IndianaJonesarr1);
			})
		})
	}
} */

/* function initHarryPotter() {
	if ($('#harrypotterMain').children().length === 0){
		$.get('IntHarryPotter', function (data) {
			$.each(data.IntHarryPotter, function ( HPkey, HPval ) {
				var HParr1 = makeGrid1(HPval);
				$('#harrypotterMain').append(HParr1);
			})
		})
	}
} */

/* function initTremors() {
	if ($('#tremorsMain').children().length === 0){
		$.get('IntTremors', function (data) {
			$.each(data.IntTremors, function (Tremorskey, Tremorsval) {
				var HParr1 = makeGrid1(Tremorsval);
				$('#tremorsMain').append(HParr1);
			})
		})
	}
} */

/* function initJohnWayne() {
	if ($('#johnwayneMain').children().length === 0){
		$.get('IntJohnWayne', function (data) {
			$.each(data.IntJohnWayne, function ( JohnWaynekey, JohnWayneval ) {
				var JohnWaynearr1 = makeGrid1(JohnWayneval);
				$('#johnwayneMain').append(JohnWaynearr1);
			})
		})
	}
} */

/* function initJurassicPark() {
	if ($('#jurassicparkMain').children().length === 0){
		$.get('IntJurassicPark', function (data) {
			$.each(data.IntJurasicPark, function (jurkey, jurval) {
				var JParr1 = makeGrid1(jurval);
				$('#jurassicparkMain').append(JParr1);
			})
		})
	}
} */

/* function initMisc() {
	if ($('#miscMain').children().length === 0){
		$.get('IntMisc', function (data) {
			$.each(data.IntMisc, function ( Misckey, Miscval ) {
				var Miscarr1 = makeGrid1(Miscval);
				$('#miscMain').append(Miscarr1);
			})
		})
	}
} */

// function initMenInBlack() {
// 	if ($('#meninblackMain').children().length === 0){
// 		$.get('IntMenInBlack', function (data) {
// 			$.each(data.IntMenInBlack, function (mibkey, mibval) {
// 				var MIBarr1 = makeGrid1(mibval);
// 				$('#meninblackMain').append(MIBarr1);	
// 			})
// 		})
// 	}
// }


// var initMtime = function () {
// 	$("#foo3, #foo4, #doneBtn, #update2").hide();
/*	initSciFi();
	initAction();
	initComedy();
	initDrama();
	initCartoons();
	initKingsman();
	initGodzilla();
	initStarTrek();
	initStarWars();
	initSuperHeros();
	initIndianaJones();
	initHarryPotter();
	initJohnWayne();
	initJurassicPark();
	initTremors();
	initMenInBlack();
	initMisc();*/
// };
// $(window).load(initMtime)
