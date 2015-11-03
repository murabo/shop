/* ===================================================================

 * スムーススクロール
 
=================================================================== */
$(function(){
   // #で始まるアンカーをクリックした場合に処理
   $('a[href^=#]').click(function() {
      // スクロールの速度
      var speed = 400;// ミリ秒
      // アンカーの値取得
      var href= $(this).attr("href");
      // 移動先を取得
      var target = $(href == "#" || href == "" ? 'html' : href);
      // 移動先を数値で取得
      var position = target.offset().top;
      // スムーススクロール
      $($.browser.safari ? 'body' : 'html').animate({scrollTop:position}, speed, 'swing');
      return false;
   });
});


/* ===================================================================

 * 画像のロールオーバー
 
=================================================================== */
$.fn.rollover = function() {
   return this.each(function() {
      // 画像名を取得
      var src = $(this).attr('src');
      //すでに画像名に「_on.」が付いていた場合、ロールオーバー処理をしない
      if (src.match('_on.')) return;
      // ロールオーバー用の画像名を取得（_onを付加）
      var src_on = src.replace(/^(.+)(\.[a-z]+)$/, "$1_on$2");
      // 画像のプリロード（先読み込み）
      $('<img>').attr('src', src_on);
      // ロールオーバー処理
      $(this).hover(
         function() { $(this).attr('src', src_on); },
         function() { $(this).attr('src', src); }
      );
   });
};


// 画像をロールオーバーする箇所を指定
$(function() {
   // $('#menu img').rollover();
   // $('form input:image').rollover();
   
   getReviewList();
});



/* ===================================================================

 * レビューを取得
 
=================================================================== */

function getReviewList(_limit, _offset){
   $.ajax({
      type: 'GET',
      url: '/api/review/'+jan+'/',
      dataType: 'json',
      success: function(data){
         var template = Handlebars.compile($('#review').html());
         // レビュー一覧
         $('.reviewList').append(template(data.ResultSet));
         // レビュー件数
         $('.reviewCnt').text(data.ResultSet.totalResultsReturned);

         if(data.ResultSet.totalResultsReturned > 3) $('.reviewLink').css({'display':'block'});

          for (var i = 1 ; i <= 3 ; i++){
            $('.reviewList > li:nth-child('+ i +')').css({'display':'block'});
          }

      }
   });

   // 口コミをもっとみるリンク
   $(".reviewLink").click(function () {
      $('.reviewList > li').css({'display':'block'});
      $('.reviewLink').css({'display':'none'});
   });

}


Handlebars.registerHelper("great", function(update) {
   var dateFormat = new DateFormat("yyyy年MM月dd日 HH時mm分");
   return dateFormat.format(new Date(update));
});

