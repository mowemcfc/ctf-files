module Main where

import Control.Concurrent (threadDelay)
import Data.Word

main :: IO ()
main = getSlowLine >>= putStrLn . process . reads

getSlowLine :: IO String
getSlowLine = do
  s <- getLine
  threadDelay 3000000
  return s

process :: [(Word64, String)] -> String
process = error "REDACTED"

data Stringer a = Letter Char a
                | End

newtype Fix f = Fix { unFix :: f (Fix f) }

toString :: Fix Stringer -> String
toString x = case unFix x of
  End -> ""
  Letter c cs -> c: toString cs

instance Functor Stringer where
  fmap f (Letter c x) = Letter c (f x)
  fmap _ End = End

ana :: Functor f => (a -> f a) -> a -> Fix f
ana gAlg x = Fix $ fmap g $ gAlg x
  where g = ana gAlg

makeFlag :: String -> String
makeFlag s = "flag{" ++ s ++ "}"

makeSecret :: Word64 -> String
makeSecret = makeFlag . toString . ana buildSecret
  where
    buildSecret :: Word64 -> Stringer Word64
    buildSecret = error "REDACTED"
