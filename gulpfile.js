var gulp = require("gulp");
var cssnano = require("gulp-cssnano");
var rename = require("gulp-rename");
var uglify = require("gulp-uglify");
var concat = require("gulp-concat");
var cache = require("gulp-cache");
var imagemin = require("gulp-imagemin");
var bs = require("browser-sync").create();
var sass = require("gulp-sass");
var util = require("gulp-util"); //js出现错误会打印错误信息
var sourcemaps = require("gulp-sourcemaps")

var path = {
    'html':'./templates/**/',
    'css': './static/css/',
    'js': './static/js/',
    'images': './static/movie/',
    'css_dist': './static/dist/css/',
    'js_dist': './static/dist/js/',
    'images_dist': './static/dist/movie/',
};

//定义处理html文件的任务(其实html也可以压缩)
gulp.task("html",function () {
    gulp.src(path.html+'*.html')
        .pipe(bs.stream())
});

//定义处理css文件的任务
gulp.task("css", function () {
    gulp.src(path.css + '*.scss')
        .pipe(sass().on("error",sass.logError))
        .pipe(cssnano())
        .pipe(rename({"suffix": ".min"}))
        .pipe(gulp.dest(path.css_dist))
        .pipe(bs.stream())
});

//定义处理js文件的任务
gulp.task("js", function () {
    gulp.src(path.js + '*.js')
        .pipe(sourcemaps.init())
        .pipe(uglify().on("error",util.log))
        .pipe(rename({"suffix": ".min"}))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.js_dist))
        .pipe(bs.stream())
});

//定义处理图片的任务
gulp.task("images", function () {
    gulp.src(path.images + '*.*')
        .pipe(cache(imagemin()))
        .pipe(gulp.dest(path.images_dist))
        .pipe(bs.stream())
});

//定义监听文件修改的任务
gulp.task("watch", function () {
    gulp.watch(path.html+'*.html',['html']);
    gulp.watch(path.css + '*.scss', ['css']);
    gulp.watch(path.js + '*.js', ['js']);
    gulp.watch(path.images + '*.*', ['images']);
});

//初始化browser-sync的任务
gulp.task("bs", function () {
    bs.init({
        'server': {
            'baseDir': './'
        }
    });
});

//创建一个默认任务,default在终端运行时不用输入名字可直接gulp运行
//gulp.task("default", ['bs', 'watch']);
gulp.task("default",['watch']);