'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var concat = require('gulp-concat');

// main styles file to compile. Its output is used on site itself
var sassMainFile = './KinaKipa/static/scss/!main.scss';

// would be content.css - file for tinymce to apply styles on articles
var sassArticleDefaultStylesFile = './KinaKipa/static/scss/!content.scss';

var sassWatchFiles = './KinaKipa/static/scss/**/*.scss';
var sassOutputFolder = './KinaKipa/static/css/';

var CC_STATIC_VERSION = 1.01;

gulp.task('default', function() {
    gulp.start('sass');
});

gulp.task('sass', function() {
    gulp.start('sassMain');
    gulp.start('sassArticle');
});

gulp.task('sassMain', function() {
     return gulp.src(sassMainFile)
        .pipe(sourcemaps.init())
        .pipe(sass().on('error', sass.logError))
        .pipe(sourcemaps.write())
        .pipe(concat('styles-' + CC_STATIC_VERSION + '.css'))
        .pipe(gulp.dest(sassOutputFolder));
});

gulp.task('sassArticle', function() {
     return gulp.src(sassArticleDefaultStylesFile)
        .pipe(sourcemaps.init())
        .pipe(sass().on('error', sass.logError))
        .pipe(sourcemaps.write())
        .pipe(concat('content-' + CC_STATIC_VERSION + '.css'))
        .pipe(gulp.dest(sassOutputFolder));
});

gulp.task('sass:watch', function () {
    gulp.watch(sassWatchFiles, ['sass']);
});

gulp.task('watch', function () {
    gulp.start('sass:watch');
});