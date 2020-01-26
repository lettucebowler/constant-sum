#!/usr/bin/env bash
  rm start end
  date +%s%3N > start
  ./constant.py -n 10 >> test10
  date +%s%3N > end
  cat start
  cat end

